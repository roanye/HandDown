import React, { useState, useEffect, useRef } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, ScrollView, TextInput, Image, SafeAreaView, FlatList, Animated } from 'react-native';
import pImage from '../assets/profilestockphoto.jpg';
import { useFocusEffect } from '@react-navigation/native';

const Profile = () => {
  const [interestTags, setInterestTags] = useState([]);
  const [givingTags, setGivingTags] = useState([]);
  const [listings, setListings] = useState([]);
  const ipAddress = '192.168.0.128';

  // useEffect(() => {
  //   // Fetch listings from the API when the component mounts
  //   const fetchListings = async () => {
  //     try {
  //       const response = await fetch(`http://${ipAddress}:8000/listings`);
  //       const data = await response.json();
  //       setListings(data);  // Assuming the API returns an array of listings
  //     } catch (error) {
  //       console.error("Error fetching listings:", error);
  //     }
  //   };

  //   fetchListings();  // Call the fetch function
  // }, []);

  useFocusEffect(
    React.useCallback(() => {
      const fetchListings = async () => {
        try {
          const response = await fetch(`http://${ipAddress}:8000/listings`);
          const data = await response.json();
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
  

  const scrollY = useRef(new Animated.Value(0)).current;
  const textYPosition = useRef(0);
  const [isSticky, setIsSticky] = useState(false);
  const textRef = useRef(null);
  const scrollViewRef = useRef(null);

  useEffect(() => {
    if (textRef.current) {
      textRef.current.measureLayout(
        scrollViewRef.current,
        (x, y) => {
          textYPosition.current = y;
        },
      );
    }
  }, []);

  const handleScroll = Animated.event(
    [{ nativeEvent: { contentOffset: { y: scrollY } } }],
    { useNativeDriver: false, }
  );

  useEffect(() => {
    const scrollListener = scrollY.addListener(({ value }) => {      
      setIsSticky(value >= (textYPosition.current));
    });

    return () => scrollY.removeListener(scrollListener);
  }, []);

  return (
    <SafeAreaView style={styles.safeAreaContainer}>
        <View style={styles.container}>
          {isSticky && (
            <View style={[styles.listingHeaderContainer, styles.stickyHeader]}>
              <Text style={styles.listingHeader}>Current Listings</Text>
            </View>
          )}

          <ScrollView
            ref={scrollViewRef}
            contentContainerStyle={styles.content}
            onScroll={handleScroll}
            scrollEventThrottle={16}
          >
            <View style={styles.profileSection}>
              <Image source={pImage} style={styles.profileImage} />
              <View style={styles.infoContainer}>
                <View style={styles.infoBox}>
                  <Text style={styles.infoText}> Ian Ryan </Text>
                </View>
                <View style={styles.infoBox}>
                  <Text style={styles.infoText2}> ian.ryan@tufts.edu </Text>
                </View>
              </View>
            </View>

            <View style={styles.tagSection}>
              <View style={styles.subsection}>
                <Text style={styles.sectionTitle}>Your Interests</Text>
                <FlatList
                  data={interestTags} // Array of user-selected tags
                  keyExtractor={(item, index) => index.toString()}
                  horizontal
                  showsHorizontalScrollIndicator={false}
                  contentContainerStyle={styles.tagsContainer}
                  renderItem={({ item }) => (
                    <TouchableOpacity style={styles.tag}>
                      <Text style={styles.tagText}>{item}</Text>
                    </TouchableOpacity>
                  )}
                />
              </View>
              
              <View style={styles.subsection}>

                <Text style={styles.sectionTitle}>What You Have to Offer</Text>
                <FlatList
                  data={givingTags}
                  keyExtractor={(item, index) => index.toString()}
                  horizontal
                  showsHorizontalScrollIndicator={false}
                  contentContainerStyle={styles.tagsContainer}
                  renderItem={({ item }) => (
                    <TouchableOpacity style={styles.tag}>
                      <Text style={styles.tagText}>{item}</Text>
                    </TouchableOpacity>
                  )}
                />
              </View>
            </View>


            <View style={styles.listingSection}>

              {!isSticky && (
                <View ref={textRef} style={styles.listingHeaderContainer}>
                  <Text style={styles.listingHeader}>Current Listings</Text>
                </View>
              )}

              <View style={{ height: isSticky ? 37 : 0, backgroundColor: "white" }} /> 

              <View style={styles.listingsContainer}>
                {listings.map((item, index) => (
                  <View key={item.id} style={[styles.listing, index % 2 === 0 ? { marginRight: '2%' } : null]}>
                    <Image
                      source={{ uri: item.imageUrl }} // Replace with your actual image URL from listing data
                      style={styles.listingImage}
                    />
                    <Text style={styles.listingText}>{item.title}</Text>
                  </View>
                ))}
              </View>
            </View>

          </ScrollView>
        </View>
    </SafeAreaView>
  );
};

export default Profile;

const styles = StyleSheet.create({
  safeAreaContainer: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  content: {
    alignItems: 'center',
    paddingVertical: 20,
    flexGrow: 1,
  },
  profileSection: {
    flexDirection: 'column',
    alignItems: 'center',
    marginBottom: 20,
    paddingVertical: 10,
    width: '90%',
    justifyContent: 'space-between',
    borderBottomColor: '#2aa4eb',
    borderBottomWidth: 1,
  },
  profileImage: {
    width: 175,
    height: 175,
    backgroundColor: '#ccc',
    borderRadius: 100,
  },
  infoContainer: {
    flex: 1,
    alignItems: 'center',
    marginTop: 10,
  },
  infoBox: {
    backgroundColor: 'transparent',
    padding: 7,
    borderRadius: 5,
  },
  infoText: {
    color: '#2aa4eb',
    fontSize: 25,
    fontFamily: 'work_sans',
  },
  infoText2: {
    color: '#2aa4eb',
    fontSize: 20,
    fontFamily: 'work_sans',
  },
  tagSection: {
    width: '90%',
    marginBottom: 20,
    borderBottomColor: "#2aa4eb",
    borderBottomWidth: 1,
  },
  subsection: {
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#2aa4eb',
    fontFamily: 'work_sans',
  },
  tagsContainer: {
    flexDirection: 'row',
    paddingHorizontal: 2,
    paddingVertical: 2,
  },
  tag: {
    backgroundColor: '#2aa4eb',
    padding: 10,
    borderRadius: 5,
    marginHorizontal: 4,
  },
  tagText: {
    color: '#ffffff',
    fontSize: 14,
    fontFamily: 'work_sans',
  },
  listingHeader: {
    fontSize: 22,
    fontWeight: 'bold',
    paddingVertical: 5,
    marginBottom: 5,
    color: '#2aa4eb',
    fontFamily: 'work_sans',
  },
  listingSection: {
    width: '90%',
    marginBottom: 20,
  },
  listingHeaderContainer: {
    backgroundColor: "white",
  },
  stickyHeader: {
    position: "absolute",
    zIndex: 100,
    width: '90%',
    alignSelf: 'center',
  },
  listingsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    width: '100%',
  },
  listing: {
    width: '49%',
    backgroundColor: '#2aa4eb',
    borderRadius: 5,
    alignItems: 'center',
    marginBottom: 10,
  },
  listingImage: {
    width: '100%',
    height: 150,
    backgroundColor: '#ccc',
    marginBottom: 5,
    borderRadius: 5,
  },
  listingText: {
    color: '#ffffff',
    fontSize: 17,
    textAlign: 'center',
    fontFamily: 'work_sans',
    paddingVertical: 5
  },
});
