// JournalCard.tsx
import React from "react";
import { View, Text, Image } from "react-native";
import { JournalCardProps } from "./types";

export const JournalCard: React.FC<JournalCardProps> = ({
  status,
  title,
  description,
  imageUrl,
  imageAlt,
}) => {
  return (
    <View style={{ 
      padding: 16, 
      marginBottom: 8, 
      backgroundColor: 'white', 
      borderRadius: 16,
      borderWidth: 1,
      borderColor: '#E5E5E5',
      boxShadow: '0px 8px 8px rgba(0, 0, 0, 0.1)',
      elevation: 4  // Keep elevation for Android support
    }}>
      <View style={{ flexDirection: 'row', alignItems: 'center', gap: 4, paddingHorizontal: 8, paddingVertical: 2, borderRadius: 999 }}>
        <Text style={{ fontSize: 12, fontWeight: '600' }}>{status}</Text>
      </View>
      <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginTop: 12 }}>
        <View style={{ flex: 1 }}>
          <Text style={{ fontSize: 14, fontWeight: '600', color: '#171717' }}>{title}</Text>
          <Text style={{ fontSize: 12, color: '#6B7280', marginTop: 4 }}>{description}</Text>
        </View>
        <Image
          source={{ uri: imageUrl }}
          accessibilityLabel={imageAlt}
          style={{ width: 52, height: 52, borderRadius: 12, objectFit: 'cover' }}
        />
      </View>
    </View>
  );
};