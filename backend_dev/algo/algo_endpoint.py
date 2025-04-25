from fastapi import APIRouter, HTTPException
import pandas as pd
import numpy as np
import random

# Similarity
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from datetime import datetime
import re

import requests


router = APIRouter()

# --- Import or define your helper functions and data loading here ---
# For example:


# ------------------------------------------------------------

# --- Helper Functions (from notebook code cells) ---

def get_listings_matrix():

    print("Getting listings matrix...")
    # Define the URL
    listings_url = "http://10.243.62.204:8000/listings/get-all-listings"

    # Send a GET request to the URL
    response = requests.get(listings_url)
    
    print("Response received!")
    # Check if the response was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # DataFrame 2: 10x12 with one column of 0's and 1's, rest empty
        listing_column_labels = [
            "Long Description", "Item Type (Category/Tags)", "Listing ID", "Listing/Request", "User ID", 
            "Price", "Date of Posting", "Title/Brief Description", "Transaction Type"
        ]

        # Initialize an empty list to hold the data for each profile
        listings_list = []

        # Loop through each profile and extract relevant fields
        for listing in data:
            if (listing.get("id", np.nan) != np.nan):
                listing_data = {
                    "Long Description": str(listing.get("long_description", np.nan)), 
                    "Item Type (Category/Tags)": str(listing.get("tags", np.nan)), 
                    "Listing ID": str(listing.get("id", np.nan)), 
                    "Listing/Request": str(listing.get("listing_type", np.nan)), 
                    "User ID": str(listing.get("profile_offerer_id", np.nan)), 
                    "Price": int(listing.get("price", np.nan)), 
                    "Date of Posting": datetime.fromisoformat(listing.get("time_created", np.nan)),                 "Title/Brief Description": str(listing.get("title", np.nan)),
                    "Transaction Type": str(listing.get("transaction_type", np.nan))
                }
                listings_list.append(listing_data)
                
        print("Listings list initialized!")

        # Convert the list of profiles to DataFrame 4 (profiles' features)
        post_features_df = pd.DataFrame(listings_list, columns=listing_column_labels)
        post_features_df = post_features_df.set_index("Listing ID", drop=False)

        # Replace "listing" with 1 and "request" with 0 in the "Listing/Request" column
        post_features_df['Listing/Request'] = post_features_df['Listing/Request'].replace({'listing': 1, 'request': 0})

        # Grab the number of listings (rows) and features (columns)
        num_listings = post_features_df.shape[0]  # Number of rows
        num_listing_features = post_features_df.shape[1]  # Number of columns

        print("Listings matrix loaded!")

        return post_features_df, num_listings, num_listing_features, listing_column_labels

    else:
        print("Failed to retrieve data:", response.status_code)


def preprocess_text(text):
    # Convert to lowercase and remove punctuation
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text


def calculate_similarity(item1_list, item2_list, listing_column_labels):
    # Extract relevant features

    item1 = pd.DataFrame([item1_list], columns=listing_column_labels)
    item2 = pd.DataFrame([item2_list], columns=listing_column_labels)

    
    title_desc1 = preprocess_text(item1["Title/Brief Description"][0] + " " + item1["Long Description"][0])  # Combine title and description
    title_desc2 = preprocess_text(item2["Title/Brief Description"][0] + " " + item2["Long Description"][0])
    price1, price2 = item1["Price"][0], item2["Price"][0]
    category1, category2 = item1["Item Type (Category/Tags)"][0], item2["Item Type (Category/Tags)"][0]
    date1, date2 = item1["Date of Posting"][0], item2["Date of Posting"][0]

    similarity_scores = []

    # Text similarity (Title and Description)
    tfidf = TfidfVectorizer().fit_transform([title_desc1, title_desc2])
    text_sim = cosine_similarity(tfidf)[0][1]
    similarity_scores.append(text_sim)

    # Price similarity
    if max(price1, price2) != 0:
        price_sim = 1 - (abs(price1 - price2) / max(price1, price2))
    else:
        price_sim = 1  # If both prices are 0, consider them identical
    similarity_scores.append(price_sim)

    # Category similarity (exact match = 1, mismatch = 0)
    category_sim = 1 if category1 == category2 else 0
    similarity_scores.append(category_sim)

    # Date similarity
    date1 = date1.replace(tzinfo=None)
    date2 = date2.replace(tzinfo=None)

    date_diff = abs((date1 - date2).days)
    # If you want to calculate the similarity score based on date_diff:
    date_sim = 1 / (1 + date_diff)  # Convert difference to similarity


    similarity_scores.append(date_sim)

    # Calculate overall similarity (weighted average)
    weights = [0.4, 0.2, 0.3, 0.1]  # text, price, category, date, NOTE: add another weight to include numerical
    overall_similarity = np.average(similarity_scores, weights=weights)
    
    return overall_similarity, similarity_scores, weights


def get_post_similarity_matrix(post_features_df, num_listings, listing_column_labels):
    # Create an empty similarity matrix with rows and columns equal to the number of listings
    similarity_matrix = np.full((num_listings, num_listings), np.nan)

    post_ids = post_features_df['Listing ID'].tolist()

    # Loop over all pairs of posts and calculate similarity
    for i in range(num_listings):
        for j in range(num_listings):
            # Get the feature vectors for post i and post j (for this example, we assume the features are in post_features_df)
            post_i = list(post_features_df.iloc[i])
            post_j = list(post_features_df.iloc[j])

            # Calculate the similarity between post_i_vector and post_j_vector
            overall_similarity, similarity_scores, weights = calculate_similarity(post_i, post_j, listing_column_labels)
            
            # Store the similarity in the matrix (symmetric matrix)
            similarity_matrix[i, j] = overall_similarity
            similarity_matrix[j, i] = overall_similarity  # Ensure symmetry

    # Create a DataFrame from the similarity matrix
    # post_similarity_df = pd.DataFrame(similarity_matrix, columns=post_features_df.index, index=post_features_df.index)
    post_similarity_df = pd.DataFrame(
        similarity_matrix,
        index=post_features_df.index,   # Post IDs as rows
        columns=post_features_df.index   # Post IDs as columns
    )
    return post_similarity_df

def get_profiles_matrix():
    print("Getting profiles matrix...")
    # Define the URL
    url = "http://10.243.62.204:8000/profile/profiles"

    # Send a GET request to the URL
    response = requests.get(url)

    print("Response received!")

    # Check if the response was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        profile_column_labels = [
            "Password", "User-ID", "Offerings", "Tufts ID", "Liked", "Interests", 
            "Image URL", "Disliked", "Messages Opened", "Last Name", "Email", "First Name", "Current Listings"
        ]

        # Initialize an empty list to hold the data for each profile
        profiles_list = []

        print("Profiles list initialized!")

        # Loop through each profile and extract relevant fields
        for profile in data:
            # print("ANOTHER ONE: \n")
            # print(profile)

            if pd.notna(profile.get("uid", np.nan)):
                profile_data = {
                    "Password": str(profile.get("password", np.nan)), 
                    "User-ID": str(profile.get("uid", np.nan)), 
                    "Offerings": str(profile.get("offerings", np.nan)), 
                    "Tufts ID": str(profile.get("tuftsid", np.nan)), 
                    "Liked": list(profile.get("Interested", np.nan)), 
                    "Interests": str(profile.get("interests", np.nan)), 
                    "Image URL": profile.get("imageUrl", np.nan), 
                    "Disliked": list(profile.get("Disliked", np.nan)), 
                    "Messages Opened": list(profile.get("SuperLiked", np.nan)), 
                    "Last Name": str(profile.get("lname", np.nan)), 
                    "Email": str(profile.get("email", np.nan)), 
                    "First Name": str(profile.get("fname", np.nan)), 
                    "Current Listings": list(profile.get("Current_listings", np.nan))
                }
                profiles_list.append(profile_data)
        # print(profiles_list)

        print("Profiles list appended!")

        # Convert the list of profiles to DataFrame 4 (profiles' features)
        profile_features_df = pd.DataFrame(profiles_list, columns=profile_column_labels)

        # Grab the number of listings (rows) and features (columns)
        num_profiles = profile_features_df.shape[0]  # Number of rows
        num_profile_features = profile_features_df.shape[1]  # Number of columns

        print("Profiles matrix loaded!")

        return profile_features_df, num_profiles, num_profile_features, profile_column_labels
    else:
        print("Failed to retrieve data:", response.status_code)


def get_ratings_matrix(profile_features_df, post_similarity_df):
    # Assuming profile_features_df is already created from your earlier code
    # Create a new DataFrame for ratings (initializing with NaN values)
    user_ids = profile_features_df['User-ID'].values

    # Collect all unique IDs from the 'Liked', 'Disliked', and 'Messages Opened' fields
    all_ids = post_similarity_df.index

    # Create a new DataFrame for ratings with NaN, 1, 2, or 3
    ratings_matrix = []

    # Loop over each user and create their ratings row
    for user_id in user_ids:
        ratings_row = []
        for post_id in all_ids:
            # Check if the post_id is in 'Liked', 'Disliked', or 'Messages Opened'
            if post_id in profile_features_df.loc[profile_features_df['User-ID'] == user_id, 'Liked'].values[0]:
                ratings_row.append(2)  # Liked = 2
            elif post_id in profile_features_df.loc[profile_features_df['User-ID'] == user_id, 'Disliked'].values[0]:
                ratings_row.append(1)  # Disliked = 1
            elif post_id in profile_features_df.loc[profile_features_df['User-ID'] == user_id, 'Messages Opened'].values[0]:
                ratings_row.append(3)  # Messages Opened = 3
            else:
                ratings_row.append(np.nan)  # NaN if the post_id is not in any of the lists

        ratings_matrix.append(ratings_row)

    # Create the ratings DataFrame
    ratings_df = pd.DataFrame(ratings_matrix, index=user_ids, columns=all_ids)

    # Display the resulting ratings DataFrame
    return ratings_df


def calc_one_listing_one_user(picked_userid, picked_postid, post_similarity_df, ratings_df): # If I want to move watched to picked_userid_watched
       # Similarity score of the new post with all the other posts
       picked_post_similarity = post_similarity_df[picked_postid].reset_index()
       picked_post_similarity.columns = ['Listing ID', 'similarity_score']

       # Movies that the target user has watched
       user_ratings = ratings_df.loc[picked_userid].dropna()
       picked_userid_watched = (
              pd.DataFrame(user_ratings)
              .reset_index()
              .rename(columns={'index': 'Listing ID', picked_userid: 'rating'})
       )

       merged = pd.merge(
        left=picked_userid_watched,
        right=picked_post_similarity,
        left_on='Listing ID',  # Use the correct column name
        right_on='Listing ID',
        how='inner'
        ).sort_values(by='similarity_score', ascending=False)

       # Calculate predicted rating
       if not merged.empty:
              predicted_rating = np.average(
              merged['rating'], 
              weights=merged['similarity_score']
              )
              return round(predicted_rating, 6)
       else:
              return 0.0


def all_listings_one_profile_rec(picked_userid, post_similarity_df, ratings_df):
    # Movies that the target user has NOT watched
    picked_userid_not_watched = pd.DataFrame(ratings_df.loc[picked_userid].isna())\
                                .reset_index()\
                                .rename(columns={picked_userid: 'not_watched'})\
                                .query("not_watched == True")\
                                .drop(columns=['not_watched'])

    # Create lists to store post_ids and predicted ratings
    post_ids = []
    predicted_ratings = []

    for val in picked_userid_not_watched.values:
        post_id = val[0]  # Assuming the post_id is the first (and only) element in val

        predicted_rating = calc_one_listing_one_user(picked_userid, post_id, post_similarity_df, ratings_df) # move picked_userid_watched inside to parameter if I want

        post_ids.append(post_id)
        predicted_ratings.append(predicted_rating)

    # Create the DataFrame
    results_df = pd.DataFrame({
        'Listing ID': post_ids,
        'predicted_rating': predicted_ratings
    })

    return results_df



# def create_experienced_feed(new_df, seen_df, post_features_df, max_seen_consecutive=2, random_factor=0.1, listing_request_ratio=0.5):
#     """
#     Creates an interleaved social media feed with controlled randomness to maintain engagement
#     while preventing predictable patterns.
#     """
#     new_list = new_df.to_dict('records')
#     seen_list = seen_df.to_dict('records')
#     feed = []
#     seen_consecutive_count = 0
#     new_index = 0
#     seen_index = 0
#     listing_count = 0
#     total_count = 0

#     while new_index < len(new_list) or seen_index < len(seen_list):
#         # Calculate current ratios
#         if total_count > 0:
#             current_listing_ratio = listing_count / total_count
#         else:
#             current_listing_ratio = 0.0

#         # Adjust listing priority based on current ratio
#         if current_listing_ratio < listing_request_ratio:
#             listing_priority = 0.7 + random_factor
#         else:
#             listing_priority = 0.3 - random_factor

#         # Determine whether to pick from new or seen
#         if seen_consecutive_count >= max_seen_consecutive:
#             pick_new = True
#         elif new_index >= len(new_list):
#             pick_new = False
#         elif seen_index >= len(seen_list):
#             pick_new = True
#         else:
#             # Check if next new post is a Listing
#             next_new_post_id = new_list[new_index]['Listing ID']
#             is_new_listing = post_features_df.loc[next_new_post_id]['Listing/Request'] == 1

#             # Adjust pick_new probability based on post type and current ratios
#             if is_new_listing:
#                 pick_new = random.random() < listing_priority
#             else:
#                 pick_new = random.random() < (1 - listing_priority)

#         # Add post to feed
#         if pick_new and new_index < len(new_list):
#             feed.append(new_list[new_index])
#             new_index += 1
#             seen_consecutive_count = 0
#         elif seen_index < len(seen_list):
#             feed.append(seen_list[seen_index])
#             seen_index += 1
#             seen_consecutive_count += 1

#         # Update counts
#         if len(feed) > 0:
#             added_post_id = feed[-1]['Listing ID']
#             if post_features_df.loc[added_post_id]['Listing/Request'] == 1:
#                 listing_count += 1
#             total_count += 1

#     # Ensure all columns are present in each feed item
#     for item in feed:
#         if 'predicted_rating' not in item:
#             item['predicted_rating'] = None
#         if 'rating' not in item:
#             item['rating'] = None

#     return pd.DataFrame(feed, columns=['Listing ID', 'predicted_rating', 'rating'])


def create_experienced_feed(new_df, seen_df, post_features_df, max_seen_consecutive=2, random_factor=0.1, listing_request_ratio=0.5):
    """
    Creates an interleaved feed with randomization from top 5 new recommendations,
    while maintaining content ratios and preventing patterns.
    """
    new_list = new_df.to_dict('records')
    seen_list = seen_df.to_dict('records')
    feed = []
    seen_consecutive_count = 0
    listing_count = 0
    total_count = 0

    while new_list or seen_list:
        # Calculate current ratios
        current_listing_ratio = listing_count / total_count if total_count > 0 else 0.0
        
        # Dynamic priority adjustment
        listing_priority = 0.7 + random_factor if current_listing_ratio < listing_request_ratio else 0.3 - random_factor

        # Determine selection type
        if seen_consecutive_count >= max_seen_consecutive:
            pick_new = True
        elif not new_list:
            pick_new = False
        elif not seen_list:
            pick_new = True
        else:
            # Check next new post type
            next_new = new_list[0]  # Peek first item (not necessarily chosen)
            is_listing = post_features_df.loc[next_new['Listing ID']]['Listing/Request'] == 1
            pick_new = random.random() < (listing_priority if is_listing else 1 - listing_priority)

        if pick_new and new_list:
            # Select from top 5 candidates
            window_size = min(5, len(new_list))
            candidates = new_list[:window_size]
            chosen = random.choice(candidates)
            
            # Add to feed and remove from pool
            feed.append(chosen)
            new_list.remove(chosen)
            seen_consecutive_count = 0
            
            # Update counts
            if post_features_df.loc[chosen['Listing ID']]['Listing/Request'] == 1:
                listing_count += 1
            total_count += 1
        elif seen_list:
            # Add seen post
            feed.append(seen_list.pop(0))
            seen_consecutive_count += 1
            
            # Update counts
            if post_features_df.loc[feed[-1]['Listing ID']]['Listing/Request'] == 1:
                listing_count += 1
            total_count += 1

    # Ensure consistent output format
    for item in feed:
        item.setdefault('predicted_rating', None)
        item.setdefault('rating', None)

    return pd.DataFrame(feed, columns=['Listing ID', 'predicted_rating', 'rating'])









def prompt_to_feature_vector(input_string):
    # Get current date
    current_date = datetime.now()

    # Create the feature vector
    feature_vector = [
        "", # "Long Description" 
        "", # "Item Type (Category/Tags)"
        -1, #  "Listing ID"
        "", # "Listing/Request"
        "", # "User ID"
        0.0, # "Price"
        datetime.fromisoformat(str(current_date)), # "Date of Posting"
        input_string, # "Title/Brief Description"
        "" # "Transaction Type"
    ]

    return feature_vector

def search_listing_similarity(post_features_df, input_prompt_vector, column_labels):
    # Initialize an empty array to store similarity scores
    similarity_scores = []
    post_ids = []

    # Iterate over the first three rows of post_features_df
    for index in range(min(4, len(post_features_df))):
        curr_row_data = post_features_df.iloc[index].tolist()

        # Calculate similarity and append to the array
        overall_sim_12, scores_12, weights = calculate_similarity(curr_row_data, input_prompt_vector, column_labels)
        similarity_scores.append(overall_sim_12)
        post_ids.append(curr_row_data[2])

    # Output ordered dataframe

    df = pd.DataFrame({
        'post_id': post_ids,
        'similarity_score': similarity_scores
    })

    df_sorted = df.sort_values(by='similarity_score', ascending=False)

    return df_sorted

def feed_main(user_id_to_check, profile_features_df, post_features_df, ratings_df, listing_column_labels):
    try:
        print(f"Starting feed_main for user {user_id_to_check}")
        print(f"Profile features shape: {profile_features_df.shape}")
        print(f"Post features shape: {post_features_df.shape}")
        print(f"Ratings shape: {ratings_df.shape}")
        
        # Ensure the user_id exists in the DataFrame.
        if (user_id_to_check in profile_features_df["User-ID"].values) and (user_id_to_check in ratings_df.index):
            print("User found in both profile and ratings data")
            # Calculate the sum of the specified features. Handle potential NaN values by filling them with 0.
            total_interactions = ratings_df.loc[user_id_to_check].notna().sum()
            print(f"Total interactions: {total_interactions}")

            if total_interactions > 20:
                print("User has high engagement, using recommendation-based feed")
                try:
                    new_ratings = all_listings_one_profile_rec(user_id_to_check, post_similarity_df, ratings_df)
                    print(f"Generated new ratings with shape: {new_ratings.shape}")
                except Exception as e:
                    print(f"Error in all_listings_one_profile_rec: {str(e)}")
                    raise

                try:
                    seen_ratings = (
                        ratings_df.loc[user_id_to_check]
                        .dropna()
                        .sort_values(ascending=False)
                        .reset_index()
                        .rename(columns={ratings_df.index.name: 'Listing ID', user_id_to_check: 'rating'})
                    )
                    print(f"Processed seen ratings with shape: {seen_ratings.shape}")
                except Exception as e:
                    print(f"Error processing seen ratings: {str(e)}")
                    raise

                try:
                    new_ratings_sorted = new_ratings.sort_values(by='predicted_rating', ascending=False)
                    seen_ratings_sorted = seen_ratings.sort_values(by='rating', ascending=False)
                    print("Sorted ratings successfully")
                except Exception as e:
                    print(f"Error sorting ratings: {str(e)}")
                    raise

                try:
                    feed_df = create_experienced_feed(new_ratings_sorted, seen_ratings_sorted, post_features_df, listing_request_ratio=0.6)
                    print(f"Generated feed with shape: {feed_df.shape}")
                    return feed_df
                except Exception as e:
                    print(f"Error in create_experienced_feed: {str(e)}")
                    raise
            else:
                print("User has low engagement, using content-based feed")
                try:
                    # Get user's interests and offerings
                    user_profile = profile_features_df[profile_features_df['User-ID'] == user_id_to_check].iloc[0]
                    interests = user_profile['Interests'] if pd.notna(user_profile['Interests']) else ""
                    offerings = user_profile['Offerings'] if pd.notna(user_profile['Offerings']) else ""
                    input_prompt = f"{interests} {offerings}".strip()
                    print(f"Generated input prompt: {input_prompt}")
                except Exception as e:
                    print(f"Error getting user profile: {str(e)}")
                    raise
                
                try:
                    # Generate feature vector from combined profile data
                    profile_vector = prompt_to_feature_vector(input_prompt)
                    print("Generated profile vector")
                except Exception as e:
                    print(f"Error generating profile vector: {str(e)}")
                    raise
                
                try:
                    # Get all unseen listings
                    unseen_listings = ratings_df.columns[ratings_df.loc[user_id_to_check].isna()].tolist()
                    print(f"Found {len(unseen_listings)} unseen listings")
                except Exception as e:
                    print(f"Error getting unseen listings: {str(e)}")
                    raise
                
                try:
                    # Calculate similarity scores for all unseen listings
                    similarity_scores = []
                    for listing_id in unseen_listings:
                        listing_data = post_features_df.loc[listing_id].tolist()
                        similarity, _, _ = calculate_similarity(listing_data, profile_vector, listing_column_labels)
                        similarity_scores.append((listing_id, similarity))
                    print("Calculated similarity scores")
                except Exception as e:
                    print(f"Error calculating similarity scores: {str(e)}")
                    raise
                
                try:
                    # Create sorted DataFrame of recommendations
                    new_ratings_sorted = pd.DataFrame(similarity_scores, 
                                                    columns=['Listing ID', 'predicted_rating'])\
                                        .sort_values('predicted_rating', ascending=False)
                    print("Created sorted recommendations")
                except Exception as e:
                    print(f"Error creating recommendations: {str(e)}")
                    raise
                
                try:
                    # Create empty seen_df since user has no interactions
                    seen_ratings_sorted = pd.DataFrame(columns=['Listing ID', 'rating'])
                    
                    # Generate feed with listing/request balancing
                    feed_df = create_experienced_feed(new_ratings_sorted, seen_ratings_sorted, 
                                                    post_features_df, listing_request_ratio=0.6)
                    print(f"Generated feed with shape: {feed_df.shape}")
                    return feed_df
                except Exception as e:
                    print(f"Error in create_experienced_feed: {str(e)}")
                    raise
        else:
            print(f"User ID {user_id_to_check} not found in profile_features_df or ratings_df")
            raise HTTPException(status_code=404, detail=f"User {user_id_to_check} not found")
    except Exception as e:
        print(f"Error in feed_main: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise e


def search_main(input_prompt, post_features_df):
    result = prompt_to_feature_vector(input_prompt)
    df_sorted = search_listing_similarity(post_features_df, result, listing_column_labels)

    return df_sorted


def update_similarity_matrix(new_listing_vector, new_listing_id, post_similarity_df, post_features_df, listing_column_labels):
    """
    Updates the similarity matrix with a new listing by adding a row and column.
    
    Args:
        new_listing_vector (list): Feature vector of the new listing
        new_listing_id (str): ID of the new listing
        post_similarity_df (pd.DataFrame): Existing similarity matrix
        post_features_df (pd.DataFrame): DataFrame containing all listing features
        listing_column_labels (list): Column labels for the feature vectors
    
    Returns:
        pd.DataFrame: Updated similarity matrix with new listing
    """
    # Calculate similarities with all existing listings
    new_similarities = []
    existing_ids = post_similarity_df.index.tolist()
    
    for listing_id in existing_ids:
        existing_vector = post_features_df.loc[listing_id].tolist()
        similarity, _, _ = calculate_similarity(new_listing_vector, existing_vector, listing_column_labels)
        new_similarities.append(similarity)
    
    # Create new row/column for the matrix
    new_row = pd.Series(
        [1.0] + new_similarities,  # 1.0 similarity to itself
        index=[new_listing_id] + existing_ids,
        name=new_listing_id
    )
    
    # Add to existing matrix
    updated_df = pd.concat([
        post_similarity_df, 
        pd.DataFrame([new_row], columns=post_similarity_df.columns)
    ])
    
    # Add the new listing to columns
    updated_df[new_listing_id] = updated_df.loc[:, existing_ids].mean(axis=1)  # Or use actual similarities
    
    return updated_df

def append_new_listing(post_features_df, new_listing_vector, listing_column_labels):
    """
    Appends a new listing to post_features_df while maintaining index consistency.
    
    Args:
        post_features_df (pd.DataFrame): Existing listings DataFrame
        new_listing_vector (list): Feature values ordered per listing_column_labels
        listing_column_labels (list): Column names for the DataFrame
        
    Returns:
        pd.DataFrame: Updated DataFrame with new listing
    """
    # Create temporary DataFrame for new listing
    new_row_df = pd.DataFrame([new_listing_vector], columns=listing_column_labels)
    
    # Set Listing ID as index (matches existing structure)
    listing_id = new_listing_vector[listing_column_labels.index("Listing ID")]
    new_row_df = new_row_df.set_index("Listing ID", drop=False)
    
    # Append using concat (recommended over deprecated append())
    return pd.concat([post_features_df, new_row_df], axis=0)


def new_listing_update_feed(new_listing_id, feed_sorted_df, post_similarity_df, ratings_df, 
                           post_features_df, listing_request_ratio=0.6, max_seen_consecutive=2, 
                           random_factor=0.1):
    """
    Inserts a new listing into the feed while maintaining new/seen and listing/request ratios.
    
    Args:
        new_listing_id (str): ID of the new listing to insert
        feed_sorted_df (pd.DataFrame): Current feed DataFrame from feed_main()
        post_similarity_df (pd.DataFrame): Post similarity matrix
        ratings_df (pd.DataFrame): User ratings matrix
        post_features_df (pd.DataFrame): Post features DataFrame
        listing_request_ratio (float): Target listing/request ratio
        max_seen_consecutive (int): Max allowed consecutive seen posts
        random_factor (float): Randomness factor for insertion
    
    Returns:
        pd.DataFrame: Updated feed DataFrame with new listing
    """
    # Calculate predicted rating
    user_id = ratings_df.index[0]  # Assuming single user feed
    predicted_rating = calc_one_listing_one_user(user_id, new_listing_id, 
                                                post_similarity_df, ratings_df)
    
    # Create new listing record
    new_listing_record = {
        'Listing ID': new_listing_id,
        'predicted_rating': predicted_rating,
        'rating': np.nan
    }
    
    # Convert feed to list of records
    feed_list = feed_sorted_df.to_dict('records')
    
    # Get post type from features
    is_listing = post_features_df.loc[new_listing_id]['Listing/Request'] == 1
    
    # Calculate current ratios
    current_stats = {
        'listing_count': sum(1 for item in feed_list 
                            if post_features_df.loc[item['Listing ID']]['Listing/Request'] == 1),
        'total_count': len(feed_list),
        'new_count': sum(1 for item in feed_list if pd.isna(item['rating']))
    }
    
    # Find optimal insertion index
    best_index = 0
    best_ratio_diff = float('inf')
    
    # Check first 5 positions or 25% of feed length
    max_check = min(5, len(feed_list)//4)
    
    for i in range(max_check + 1):
        temp_feed = feed_list[:i] + [new_listing_record] + feed_list[i:]
        
        # Calculate new ratios
        new_listing_count = current_stats['listing_count'] + (1 if is_listing else 0)
        new_total = current_stats['total_count'] + 1
        new_ratio = new_listing_count / new_total
        
        # Calculate ratio difference from target
        ratio_diff = abs(new_ratio - listing_request_ratio)
        
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_index = i
    
    # Insert at best position found
    updated_feed = feed_list[:best_index] + [new_listing_record] + feed_list[best_index:]
    
    # Maintain DataFrame structure
    return pd.DataFrame(updated_feed, columns=['Listing ID', 'predicted_rating', 'rating'])



# --- If you want to run as a script ---

# if __name__ == "__main__":
#     user_id = "DlIQoTG7GhGfnQRRMEVW"

#     search_prompt = "can opener"

#     # -------- Feed

#     post_features_df, num_listings, num_listing_features, listing_column_labels = get_listings_matrix()

#     post_similarity_df = get_post_similarity_matrix(post_features_df, num_listings, listing_column_labels)

#     profile_features_df, num_profiles, num_profile_features, profile_column_labels = get_profiles_matrix()

#     ratings_df = get_ratings_matrix(profile_features_df, post_similarity_df)

#     feed_sorted = feed_main(user_id, profile_features_df, post_features_df, ratings_df, listing_column_labels)

#     print("Feed: ")

#     print(feed_sorted)

#     # -------- Search

#     print("Search: ")

#     search_sorted = search_main(search_prompt, post_features_df)

#     print(search_sorted)





# ------------------------------------------------------------

# Add these as global variables
post_features_df = None
num_listings = None
num_listing_features = None
listing_column_labels = None
profile_features_df = None
num_profiles = None
num_profile_features = None
profile_column_labels = None
post_similarity_df = None
ratings_df = None

def load_data():
    global post_features_df, num_listings, num_listing_features, listing_column_labels
    global profile_features_df, num_profiles, num_profile_features, profile_column_labels
    global post_similarity_df, ratings_df
    
    try:
        print("Loading listings data...")
        post_features_df, num_listings, num_listing_features, listing_column_labels = get_listings_matrix()
        if post_features_df is None or num_listings == 0:
            raise Exception("Failed to load listings data or no listings found")
        print(f"Loaded {num_listings} listings")
        
        print("Loading profiles data...")
        profile_features_df, num_profiles, num_profile_features, profile_column_labels = get_profiles_matrix()
        if profile_features_df is None or num_profiles == 0:
            raise Exception("Failed to load profiles data or no profiles found")
        print(f"Loaded {num_profiles} profiles")
        
        print("Calculating similarity matrix...")
        post_similarity_df = get_post_similarity_matrix(post_features_df, num_listings, listing_column_labels)
        if post_similarity_df is None or post_similarity_df.empty:
            raise Exception("Failed to calculate similarity matrix")
        print("Similarity matrix calculated successfully")
        
        print("Creating ratings matrix...")
        ratings_df = get_ratings_matrix(profile_features_df, post_similarity_df)
        if ratings_df is None or ratings_df.empty:
            raise Exception("Failed to create ratings matrix")
        print("Ratings matrix created successfully")
        
        print("Data loading complete!")
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")

@router.get("/feed/{user_id}")
async def get_feed(user_id: str):
    try:
        print(f"Starting feed generation for user {user_id}")
        # Load data if not already loaded
        if post_features_df is None or post_similarity_df is None or ratings_df is None:
            print("Loading data for the first time...")
            load_data()
        
        # Validate data is loaded
        if post_features_df is None or post_similarity_df is None or ratings_df is None:
            raise HTTPException(status_code=500, detail="Failed to load required data")
        
        print("Checking if user exists in profile data...")
        if user_id not in profile_features_df["User-ID"].values:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found in profiles")
        
        print("Checking if user exists in ratings data...")
        if user_id not in ratings_df.index:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found in ratings")
        
        print("Starting feed generation...")
        # Call your feed function and return the result
        feed_df = feed_main(user_id, profile_features_df, post_features_df, ratings_df, listing_column_labels)
        
        if feed_df is None:
            raise HTTPException(status_code=500, detail="Failed to generate feed")
        
        print("Converting feed to JSON...")
        # Convert DataFrame to JSON
        if isinstance(feed_df, pd.DataFrame):
            feed_df = feed_df.replace({np.nan: None})
            return feed_df.to_dict(orient="records")
        return {"error": "No feed found"}
    except HTTPException as he:
        print(f"HTTP Exception: {str(he)}")
        raise he
    except Exception as e:
        print(f"Unexpected error in feed generation: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error generating feed: {str(e)}")

@router.get("/search/{query}")
async def search(query: str):
    # Load data if not already loaded
    if post_features_df is None:
        load_data()
        
    # Call your search function and return the result
    search_df = search_main(query, post_features_df)
    if isinstance(search_df, pd.DataFrame):
        return search_df.to_dict(orient="records")
    return {"error": "No search results found"}