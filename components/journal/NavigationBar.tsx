// NavigationBar.tsx
import React from "react";
import { View, Text } from "react-native";
import { NavigationItemProps } from "./types";

const navigationItems: NavigationItemProps[] = [
  { icon: <View />, label: "" },
  { icon: <View />, label: "" },
  { icon: <View />, label: "Journal", isActive: true },
  { icon: <View />, label: "" },
  { icon: <View />, label: "" },
];

export const NavigationBar: React.FC = () => {
  return (
    <View style={{ position: 'absolute', bottom: 0, width: '100%', maxWidth: 375, backgroundColor: 'white', paddingVertical: 16 }}>
      <View style={{ flexDirection: 'row', justifyContent: 'space-around' }}>
        {navigationItems.map((item, index) => (
          <View key={index} style={{ alignItems: 'center', gap: 4 }}>
            {item.icon}
            {item.label ? (
              <Text style={{ fontSize: 12, color: '#6B7280' }}>{item.label}</Text>
            ) : null}
          </View>
        ))}
      </View>
    </View>
  );
};