// JournalScreen.tsx
import React from "react";
import { View, Text, ScrollView } from "react-native";
import { DaySelector } from "./DaySelector";
import { JournalCard } from "./JournalCard";
import { NavigationBar } from "./NavigationBar";

const journalEntries = [
  {
    status: "planned" as const,
    title: "Eat Dry Ramen",
    description: "Make a dry ramen vegan for dinner",
    imageUrl: "https://placehold.co/52x52/f4d03f/f4d03f",
    imageAlt: "Ramen",
  },
  {
    status: "completed" as const,
    title: "Pumpkin Chicken Curry",
    description: "Make for a lunch time",
    imageUrl: "https://placehold.co/52x52/e67e22/e67e22",
    imageAlt: "Curry",
  },
  {
    status: "completed" as const,
    title: "Running 4K",
    description: "Exercise running at park center",
    imageUrl: "https://placehold.co/52x52/3498db/3498db",
    imageAlt: "Running",
  },
];

export const JournalScreen: React.FC = () => {
  return (
    <View style={{ flex: 1, backgroundColor: 'white', maxWidth: 375, margin: 'auto' }}>
      <View style={{ flexDirection: 'row', justifyContent: 'space-between', padding: 10 }}>
        <Text style={{ fontWeight: '600' }}>9:41</Text>
        <View style={{ flexDirection: 'row', gap: 8 }} />
      </View>
      <View style={{ flex: 1, backgroundColor: '#FFF1F2', borderTopLeftRadius: 24, borderTopRightRadius: 24 }}>
        <View style={{ padding: 20, backgroundColor: '#FFF1F2' }}>
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
            <Text style={{ fontSize: 18, fontWeight: 'bold', color: '#171717' }}>Journal</Text>
            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 12 }}>
              <View style={{ flexDirection: 'row', backgroundColor: 'white', borderWidth: 1, borderColor: '#FB7185', borderRadius: 999, padding: 4 }}>
                <View style={{ paddingHorizontal: 16, paddingVertical: 4 }}>
                  <Text style={{ fontSize: 14, color: '#6B7280' }}>Day</Text>
                </View>
                <View style={{ paddingHorizontal: 16, paddingVertical: 4 }}>
                  <Text style={{ fontSize: 14, color: '#6B7280' }}>Week</Text>
                </View>
              </View>
            </View>
          </View>
          <DaySelector />
        </View>
        <ScrollView style={{ backgroundColor: 'white', padding: 16 }}>
          {journalEntries.map((entry, index) => (
            <JournalCard key={index} {...entry} />
          ))}
        </ScrollView>
        <NavigationBar />
      </View>
    </View>
  );
};