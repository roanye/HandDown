import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerTitle: "Proof of Concept", // Set the header title here
      }}
    />
  );
}
