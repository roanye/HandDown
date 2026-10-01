import React, { useState, useEffect, useRef } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Image, SafeAreaView, Modal, FlatList, ActivityIndicator, ImageBackground } from 'react-native';
import Swiper from 'react-native-deck-swiper';
import backgroundPattern from "../assets/background_images/papyrus.png";

const Feed = ({ navigation }) => {
  const [loading, setLoading] = useState(true);
  const [listings, setListings] = useState([]);
  const [cardIndex, setCardIndex] = useState(0);
  const swiperRef = useRef(null);
  const [currListingTags, setCurrListingTags] = useState(["Books", "Clothes", "Accessories"]);
  const [expandedListingModalVisible, setExpandedListingModalVisible] = useState(false);
  const ipAddress = '192.168.0.128';

  const fetchListings = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://${ipAddress}:8000/listings`);
      const data = await response.json();
      // console.log("listings: ", data);
      setListings(data);
    } catch (error) {
      console.error("Error fetching listings:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchListings();
  }, []);

  const handleSwipeLeft = (index) => {
    console.log('Disliked:', listings[index].title);
    alert("Image disliked!");
  };

  const handleSwipeRight = (index) => {
    console.log('Liked:', listings[index].title);
    alert("Image liked!");
  };

  const handleSwipeDown = (index) => {
    console.log('Started conversation with:', listings[index].title);
    alert("Started conversation with", listings[index].title);
    navigation.navigate('Messaging');
  };

  const handleSwipeUp = (index) => {
    console.log('Expanded listing:', listings[index].title);
    setExpandedListingModalVisible(true);
    setCardIndex(index);

    if (swiperRef.current) {
      swiperRef.current.swipeBack();
    }
  };

  return (
    <ImageBackground source={backgroundPattern} style={styles.container} resizeMode="cover">
      <SafeAreaView style={{flex: 1}}>
        {loading ? (
          <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center'}}>
            <ActivityIndicator
              size="large"
              color="#846425"
            />
          </View>
        ) : listings.length > 0 ? (
          <Swiper 
            ref={swiperRef}
            cards={listings}
            cardIndex={cardIndex}
            renderCard={(item) =>
              item ? (
                <View style={styles.feedContent}>
                  <View style={styles.listingImage}>
                    {item.imageUrl ? (
                      <Image
                        source={{ uri: item.imageUrl }}
                        style={styles.lImage}
                        resizeMode="cover"
                      />
                    ) : (
                      <Text style={styles.listingImageText}>Listing Image</Text>
                    )}
                  </View>
                  <TouchableOpacity style={styles.profilePictureContainer}>
                    <View style={styles.profilePicture}>
                      <Image
                        source={require("../assets/profilestockphoto.jpg")}
                        style={styles.pImage}
                      />
                    </View>
                  </TouchableOpacity>
                  <View style={styles.listingInfo}>
                    <Text style={styles.listingInfoText}>
                      {item.title || "Abbreviated Listing Info"}
                    </Text>
                  </View>
                </View>
              ) : (
                <View>
                  <Text style={styles.listingInfoText}>Loading...</Text>
                </View>
              )
            }
            onSwipedLeft={handleSwipeLeft}
            onSwipedRight={handleSwipeRight}
            onSwipedTop={handleSwipeUp}
            onSwipedBottom={handleSwipeDown}
            stackSize={3}
            containerStyle={{backgroundColor: 'transparent'}}
            horizontalSwipe={true}
            verticalSwipe={true}
          />
        ) : (
          <Text style={{ textAlign: "center", marginTop: 20 }}>
            No listings available
          </Text>
        )}
    
        {/* Expanded Listing Modal */}
        <Modal
          animationType="slide"
          transparent={true}
          visible={expandedListingModalVisible}
          onRequestClose={() => setExpandedListingModalVisible(false)}
        >
          <View style={styles.modalOverlay}>
            <View style={styles.modalContent}>
              <View>
                <Text style={styles.modalTitle}>Description:</Text>
                <Text style={styles.longDescription}>
                  Blah blah blah blah blah blah blah blah blah blah blah blah blah
                  blah blah blah blah blah blah blah blah blah blah blah blah blah
                  blah blah blah blah blah blah blah.
                </Text>
              </View>
              <View>
                <Text style={styles.modalTitle}>Tags:</Text>
                {currListingTags.length > 0 ? (
                  <View style={styles.selectedTagsSection}>
                    <FlatList
                      data={currListingTags}
                      keyExtractor={(item) => item}
                      horizontal
                      showsHorizontalScrollIndicator={false}
                      renderItem={({ item }) => (
                        <View style={styles.selectedTagContainer}>
                          <Text style={styles.selectedTagText}>{item}</Text>
                        </View>
                      )}
                    />
                  </View>
                ) : null}
              </View>
              <TouchableOpacity
                style={styles.closeButton}
                onPress={() => setExpandedListingModalVisible(false)}
              >
                <Text style={styles.closeButtonText}>Close</Text>
              </TouchableOpacity>
            </View>
          </View>
        </Modal>
      </SafeAreaView>
    </ImageBackground>
  );  
};

export default Feed;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
  feedContent: {
    backgroundColor: 'transparent',
    alignSelf: 'center',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 35,
    width: '100%',
    height: '85%',
    borderRadius: 5,
  }, 
  listingImage: {
    // flex: 1,
    width: '100%',
    height: '100%',
    backgroundColor: 'transparent',
    justifyContent: 'flex-start',
    borderRadius: 5,
  },
  lImage: {
    width: '100%',
    height: '100%',
    borderRadius: 5,
  },
  listingImageText: {
    color: '#ffffff',
    fontSize: 30,
    fontWeight: 'bold',
    fontFamily: 'work_sans',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    justifyContent: "center",
    alignItems: "center",
    paddingBottom: 100
  },
  modalContent: {
    backgroundColor: "#fff",
    padding: 20,
    borderRadius: 10,
    width: "100%",
    height: "50%",
    alignItems: "left",
    justifyContent: "space-between"
  },
  modalTitle: {
    fontSize: 25,
    fontWeight: "bold",
    fontFamily: 'work_sans',
    alignSelf: 'left',
  },
  longDescription: {
    marginVertical: 15,
    backgroundColor: '#f5f5f5',
    // borderWidth: 1,
    borderRadius: 5,
    padding: 10,
    color: '#000000',
    fontSize: 16,
    fontFamily: 'work_sans',
  },
  selectedTagsSection: {
    width: '100%',
    marginTop: 10,
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  selectedTagContainer: {
    backgroundColor: '#2aa4eb',
    borderRadius: 15,
    padding: 10,
    margin: 5,
  },
  selectedTagText: {
    color: '#fff',
    fontSize: 16,
    fontFamily: 'work_sans',
  },
  closeButton: {
    marginTop: 15,
    padding: 10,
    backgroundColor: "#846425",
    borderRadius: 5,
    alignSelf: 'center',
  },
  closeButtonText: {
    color: "#fff",
    fontSize: 25,
    fontFamily: 'work_sans',
  },
  profilePictureContainer: {
    position: 'absolute',
    top: 20, 
    right: 20,
    width: 80,
    height: 80,
    borderRadius: 40,
    overflow: 'hidden',
    borderColor: '#fff',
    borderWidth: 2,
  },
  profilePicture: {
    width: '100%',
    height: '100%',
    backgroundColor: '#ffffff', 
    borderRadius: 40, 
  },
  pImage: {
    width: 76,
    height: 76,
  },
  listingInfo: {
    position: 'absolute', // Overlay on top of the image
    bottom: 0, // Stick to the bottom
    left: 0, // Ensure it spans the full width
    width: '100%', // Full width of the parent container
    height: 94, // Maintain the fixed height
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)', // Semi-transparent blue background
    borderBottomLeftRadius: 5,  // Round only bottom-left
    borderBottomRightRadius: 5, // Round only bottom-right
  },
  listingInfoText: {
    color: '#fff', 
    fontSize: 25,
    fontFamily: 'work_sans',
    fontWeight: 'bold',
  },
});
