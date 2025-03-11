import React, { useState, useEffect} from 'react';
import { StyleSheet, Text, View, TextInput, FlatList, Image, TouchableOpacity, SafeAreaView, ImageBackground } from 'react-native';
import backgroundPattern from "../assets/background_images/papyrus.png";
import { useFocusEffect } from '@react-navigation/native';

const FSearch = () => {
  const [listings, setListings] = useState([]);
  const ipAddress = '192.168.0.128';

  useFocusEffect(
    React.useCallback(() => {
      const fetchListings = async () => {
        try {
          const response = await fetch(`http://${ipAddress}:8000/listings`);
          const data = await response.json();
          // console.log("Fetched Listings:", JSON.stringify(data, null, 2)); 
          setListings(data);  // Assuming the API returns an array of listings
        } catch (error) {
          console.error("Error fetching listings:", error);
        }
      };
  
      fetchListings();  // Fetch listings when the screen comes into focus
  
      return () => {
        // Optionally, clean up if needed when the screen goes out of focus
      };
    }, [])  // Empty dependency array means it only runs when the screen is focused
  );

  return (
    <ImageBackground source={backgroundPattern} style={styles.container} resizeMode="cover">
      <SafeAreaView>
        <View style={styles.searchBarContainer}>
          <TextInput style={styles.searchBar} 
            placeholder="Search..."
            placeholderTextColor= '#737373'
          />
          <TouchableOpacity style={styles.searchIcon}>
            <Text>🔍</Text>
          </TouchableOpacity>
        </View>

        {/* <Text style={styles.suggestedQueries}>Suggested queries</Text> */}

        <View style={styles.listingsSection}>
          <FlatList
            data={listings}
            keyExtractor={(item) => item.id}
            numColumns={2} // FlatList automatically handles wrapping with numColumns
            contentContainerStyle={styles.listingsContainer} // No need for flexWrap here
            showsVerticalScrollIndicator={false}
            removeClippedSubviews={false} // Prevents images from being unloaded
            renderItem={({ item }) => (
              <View style={styles.listing}>
                {item.imageUrl ? (
                  <Image 
                    source={{uri: item.imageUrl}} 
                    style={styles.listingImage} 
                  />
                ) : (
                  <View style={[styles.listingImage, styles.placeholderImage]} />
                )}
                <View style={styles.listingTextContainer}>
                  <Text style={styles.listingText}>{item.title}</Text>
                </View>
              </View>
            )}
          />
        </View>    
      </SafeAreaView>
    </ImageBackground>
  );
};

export default FSearch;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
  },
  searchBarContainer: {
    flexDirection: 'row',
    width: '95%',
    backgroundColor: '#f5f5f5',
    borderRadius: 5,
    marginBottom: 10,
    alignItems: 'center',
    paddingHorizontal: 10,
  },
  searchBar: {
    flex: 1,
    height: 40,
    fontSize: 20,
    fontFamily: 'work_sans',
    color: '#000000',
  },
  searchIcon: {
    padding: 5,
  },
  // suggestedQueries: {
  //   alignSelf: 'flex-start',
  //   marginLeft: 20,
  //   marginBottom: 10,
  //   fontWeight: 'bold',
  //   fontFamily: 'work_sans',
  //   fontSize: 18,
  // },
  listingsSection: {
    alignItems: 'center',
    width: '95%',
    marginBottom: 20,
  },
  listingsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    width: '100%',
    paddingBottom: 85,  // Add padding at the bottom to prevent items from being cut off
  },
  listing: {
    width: '48%', // Adjust the width slightly to fit more space
    backgroundColor: '#2aa4eb',
    borderRadius: 5,
    alignItems: 'center',
    marginBottom: 10,
    marginRight: '1%', // Add space between the listings on the right side
    marginLeft: '1%', // Add space between the listings on the left side
  },  
  listingImage: {
    width: '100%',
    height: 150,
    backgroundColor: '#ccc',
    marginBottom: 5,
    borderRadius: 5,
    resizeMode: 'cover',
  },
  placeholderImage: {
    backgroundColor: '#000000',
  },
  listingTextContainer: {
    justifyContent: 'center',
    alignItems: 'center',
    flex: 1,
    // height: 30,
  },
  listingText: {
    color: '#ffffff',
    fontSize: 17,
    textAlign: 'center',
    fontFamily: 'work_sans',
    padding: 5,
  },
});