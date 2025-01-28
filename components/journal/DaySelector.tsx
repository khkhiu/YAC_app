// DaySelector.tsx
import React from "react";
import { View, Text } from "react-native";
import { DayProps } from "./types";

const days: DayProps[] = [
  { day: "M", date: "29" },
  { day: "T", date: "30", isActive: true },
  { day: "W", date: "01" },
  { day: "T", date: "02" },
  { day: "F", date: "03" },
  { day: "S", date: "04" },
  { day: "S", date: "05" },
];

export const DaySelector: React.FC = () => {
  return (
    <View style={{ flexDirection: 'row', justifyContent: 'space-between', paddingHorizontal: 16 }}>
      {days.map((item, index) => (
        <View key={index} style={{ alignItems: 'center', gap: 8 }}>
          <Text style={{ fontSize: 14, color: '#171717' }}>{item.day}</Text>
          <View style={[
            { height: 30, width: 30, borderRadius: 999, justifyContent: 'center', alignItems: 'center' },
            item.isActive && { 
              backgroundColor: '#FB7185',
              boxShadow: '0px 4px 4px rgba(0, 0, 0, 0.1)',
              elevation: 2 // Keep elevation for Android
            }
          ]}>
            <Text style={[
              { fontSize: 16, fontWeight: '600' },
              item.isActive && { color: 'white' }
            ]}>{item.date}</Text>
          </View>
        </View>
      ))}
    </View>
  );
};