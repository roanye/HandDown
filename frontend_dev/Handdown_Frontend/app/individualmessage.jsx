import React from 'react';
import { StyleSheet, Text, View, Image, TouchableOpacity, SafeAreaView } from 'react-native';

const Conversation = ({ route, navigateBack }) => {
  const { userName, listingName, listingImage } = route.params;

  return (
    <SafeAreaView style={styles.safeAreaContainer}>
        <View style={styles.container}>
            <TouchableOpacity onPress={navigateBack} style={styles.backButtonContainer}>
                <Text style={styles.backButton}>Back</Text>
            </TouchableOpacity>

            <Text style={styles.title}>Chat with {userName}</Text>
            <Text style={styles.subtitle}>About: {listingName}</Text>
            <Image source={listingImage} style={styles.listingImage} />
        </View>
    </SafeAreaView>
  );
};

export default Conversation;

const styles = StyleSheet.create({
  safeAreaContainer: {
      flex: 1,
      backgroundColor: '#ffffff',
  },
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#D3E8FF',
    position: 'relative',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    marginBottom: 20,
  },
  listingImage: {
    width: 100,
    height: 100,
    borderRadius: 10,
  },
  backButtonContainer: {
    position: 'absolute',
    top: 20,
    left: 20,
  },
  backButton: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#007BFF',
  },
});
