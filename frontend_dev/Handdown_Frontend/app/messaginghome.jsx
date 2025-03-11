import React from 'react';
import { StyleSheet, Text, View, FlatList, Image, TouchableOpacity, SafeAreaView } from 'react-native';

import image1 from '../assets/images/canopener.jpg';
import image2 from '../assets/images/suitjacket.jpg';
import image3 from '../assets/images/textbooks.jpg';
import image4 from '../assets/images/grinch_costume.jpg';
import image5 from '../assets/images/lamp.jpg';
import image6 from '../assets/images/soccer_ball.jpg';
import image7 from '../assets/images/rain_jacket.jpg';
import image8 from '../assets/images/backpack.jpg';
import image9 from '../assets/images/groceries.jpg';
import image10 from '../assets/images/thanksgiving-leftovers.jpg';

import pImage from '../assets/profilestockphoto.jpg';

const messages = [
  { id: '1', name: 'User 1', listingName: 'Can Opener', profileImage: pImage, listingImage: image1 },
  { id: '2', name: 'User 2', listingName: 'Suit Jacket', profileImage: pImage, listingImage: image2 },
  { id: '3', name: 'User 3', listingName: 'Textbooks', profileImage: pImage, listingImage: image3 },
  { id: '4', name: 'User 4', listingName: 'Grinch Halloween Costume', profileImage: pImage, listingImage: image4 },
  { id: '5', name: 'User 5', listingName: 'Desktop Lamp', profileImage: pImage, listingImage: image5 },
  { id: '6', name: 'User 6', listingName: 'Soccer Ball', profileImage: pImage, listingImage: image6 },
  { id: '7', name: 'User 7', listingName: 'Extra Rain Jacket', profileImage: pImage, listingImage: image7 },
  { id: '8', name: 'User 8', listingName: 'Backpack', profileImage: pImage, listingImage: image8 },
  { id: '9', name: 'User 9', listingName: 'Groceries', profileImage: pImage, listingImage: image9 },
  { id: '10', name: 'User 10', listingName: 'Thanksgiving Leftovers', profileImage: pImage, listingImage: image10 },
];

const Messaging = ({ navigateToConversation }) => {
  const renderMessageItem = ({ item }) => (
  <TouchableOpacity 
        style={styles.messageItem}
        onPress={() => navigateToConversation({
            userId: item.id,
            userName: item.name,
            listingName: item.listingName,
            listingImage: item.listingImage,
        })}
    >
    
    <Image source={item.profileImage} style={styles.userImage} />

    <View style={styles.messageInfo}>
      <Text style={styles.userName}>{item.name}</Text>
      <Text style={styles.listingName}>{item.listingName}</Text>
    </View>

    <Image source={item.listingImage} style={styles.listingImage} />
  </TouchableOpacity>
);

  return (
    <SafeAreaView style={styles.safeAreaContainer}>
        <View style={styles.container}>
          <TouchableOpacity>
            <Text style={styles.parkinglot}>Listings you're interested in!</Text>
          </TouchableOpacity>
          <Text style={styles.messagesLabel}> Current conversations:</Text>
          <FlatList
            data={messages}
            renderItem={renderMessageItem}
            keyExtractor={(item) => item.id}
            style={styles.messageList}
          />
        </View>
    </SafeAreaView>
  );
};

export default Messaging;

const styles = StyleSheet.create({
  safeAreaContainer: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  parkinglot: {
    marginTop: 25,
    marginBottom: 25,
    marginLeft: 10,
    width: '95%',
    justifyContent: 'center',
    padding: 20,
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
    backgroundColor: '#2aa4eb',
    borderRadius: 10,
    fontFamily: 'work_sans',
    color: "#ffffff"
  },
  messageList: {
    flex: 1,
    paddingHorizontal: 10,
  },
  messageItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 15,
    marginVertical: 5,
    backgroundColor: '#846425',
    borderRadius: 8,
  },
  listingImage: {
    width: 50,
    height: 50,
    borderRadius: 5,
  },  
  userImage: {
    width: 50,
    height: 50,
    borderRadius: 25,
  },
  messageInfo: {
    flex: 1,
    marginLeft: 15,
    alignItems: 'flex-start',
    justifyContent: 'center',
  },
  userName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#ffffff',
    fontFamily: 'work_sans',
  },
  listingName: {
    fontSize: 14,
    color: '#ffffff',
    fontFamily: 'work_sans',
  },
  messagesLabel: {
    alignSelf: 'flex-start',
    marginLeft: 10,
    marginBottom: 10,
    fontWeight: 'bold',
    fontSize: 20,
    fontFamily: 'work_sans',
  },
});
