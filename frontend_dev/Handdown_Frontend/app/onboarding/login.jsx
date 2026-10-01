import React, { useState } from 'react';
import { StyleSheet, Text, View, SafeAreaView, TouchableOpacity, TextInput } from 'react-native';

const Login = ({ navigateTo }) => {
  const [emailText, setEmailText] = useState(''); // State to store the input value
  const [passwordText, setPasswordText] = useState(''); // State to store the input value

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.whiteBackground}>

        {/* Header */}
        <View style={styles.logo}>
          <Text style={styles.logoText}>Welcome Back to Handdown!</Text>
        </View>

        <View style={styles.content}>
          {/* Top Half Content */}
          <View style={styles.topHalfContent}>
            <TextInput
            style={styles.inputBoxes}
            placeholder="Email"
            placeholderTextColor= '#737373'
            value={emailText}
            onChangeText={(text) => setEmailText(text)} // Updates state as the text changes
            />
            <TextInput
            style={styles.inputBoxes}
            placeholder="Password"
            placeholderTextColor= '#737373'
            value={passwordText}
            onChangeText={setPasswordText} // Updates state as the text changes
            />
            <TouchableOpacity 
              style={styles.loginButton} 
              onPress={() => navigateTo('Main')}
            >
              <Text style={styles.loginText}>Login</Text>
            </TouchableOpacity>
            <TouchableOpacity 
              style={styles.forgetPasswordButton} 
              onPress={() => navigateTo('ForgetPassword')}
            >
              <Text style={styles.forgetPasswordText}>Forgot your password?</Text>
            </TouchableOpacity>
          </View>

          {/* Bottom Half Content */}
          <View style={styles.bottomHalfContent}>

            <TouchableOpacity 
              style={styles.signUpButton} 
              onPress={() => navigateTo('SignUp')}
            >
              <Text style={styles.signUpText}>First Time User? Click Here to Sign Up</Text>
            </TouchableOpacity>

          </View>
        </View>
        
      </View>
    </SafeAreaView>
  );
};

export default Login;

// white: '#ffffff'
// blue: '#2aa4eb'
// brown: '#846425'
const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  whiteBackground: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  logo: {
    marginTop: 150,
    backgroundColor: '#ffffff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoText: {
    color: '#2aa4eb',
    fontSize: 30,
    fontWeight: 'bold',
    textAlign: 'center',
    fontFamily: 'work_sans',
  },
  content: {
    flex: 1,
    alignItems: 'left',
    justifyContent: 'center',
    paddingHorizontal: 20,
  },
  topHalfContent: {
    flex: 1, // Each half takes up half the height of the parent
    alignItems: 'left', // Center content horizontally
    width: '100%', // Ensure it stretches the full width'
    marginTop: 50,
  },
  inputBoxes: {
    height: 40,
    width: '100%',
    borderColor: '#000',
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderRadius: 5,
    paddingHorizontal: 10,
    height: 50,
    marginBottom: 16,
    fontFamily: 'work_sans',
    fontSize: 20,
  },
  loginButton: {
    backgroundColor: '#846425',
    borderColor: '#ffffff',
    borderWidth: 1,
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 25,
    alignItems: 'center',
    marginTop: 5,
    width: '100%',
  },
  loginText: {
    color: '#fff',
    fontSize: 22,
    fontWeight: 'bold',
    fontFamily: 'work_sans'
  },
  forgetPasswordButton: {
    backgroundColor: 'transparent',
    marginTop: 20,
  },
  forgetPasswordText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2aa4eb',
    marginBottom: 20,
    textAlign: 'left',
    fontFamily: 'work_sans'
  },
  bottomHalfContent: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
    width: '100%',
    marginBottom: 40,
  },
  signUpButton: {
    backgroundColor: '#2aa4eb',
    borderColor: '#000',
    borderWidth: 1,
    paddingVertical: 20,
    paddingHorizontal: 20,
    borderRadius: 25,
    alignItems: 'center',
    width: '100%',
  },
  signUpText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: 'bold',
    fontFamily: 'work_sans'
  },
});
