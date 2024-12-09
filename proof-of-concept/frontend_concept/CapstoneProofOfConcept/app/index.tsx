import React, { useState } from "react";
import { View, Text, TouchableOpacity, Image, StyleSheet } from "react-native";

export default function Index() {
  const [imageUri, setImageUri] = useState<string | null>(null);

  const fetchImage = async () => {
    try {
      const listingId = "FxviZDunH2dogL0c54Ps";  
      const response = await fetch(`http://127.0.0.1:8000/listings/${listingId}`);
      const data = await response.json(); // Parse the response as JSON
  
      // Check if the image_url is returned and set it to state
      if (data.image_url) {
        setImageUri(data.image_url); // Set the image URL to state for display
      } else {
        console.error("Error: Image URL not found.");
      }
    } catch (error) {
      console.error("Error fetching image:", error); // Handle any errors
    }
  };

  const closeImage = () => {
    setImageUri(null); // Set the imageUri to null to hide the image
  };

  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.button} onPress={fetchImage}>
        <Text style={styles.buttonText}>Fetch Image</Text>
      </TouchableOpacity>

      {imageUri && (
        <>
          <Image source={{ uri: imageUri }} style={styles.image} />
          <TouchableOpacity style={styles.closeButton} onPress={closeImage}>
            <Text style={styles.closeButtonText}>Close Image</Text>
          </TouchableOpacity>
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  button: {
    backgroundColor: "#ffffff",
    borderColor: "#000000",
    borderWidth: 2,
    borderRadius: 8,
    paddingVertical: 10,
    paddingHorizontal: 20,
    alignItems: "center",
  },
  buttonText: {
    color: "#000000",
    fontSize: 16,
    fontWeight: "bold",
  },
  image: {
    marginTop: 20,
    width: 100,
    height: 100,
  },
  closeButton: {
    marginTop: 20,
    backgroundColor: "#ff0000",  // Red color for the close button
    borderColor: "#000000",
    borderWidth: 2,
    borderRadius: 8,
    paddingVertical: 10,
    paddingHorizontal: 20,
    alignItems: "center",
  },
  closeButtonText: {
    color: "#ffffff",  // White text for the close button
    fontSize: 16,
    fontWeight: "bold",
  },
});
