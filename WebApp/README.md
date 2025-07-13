# Nutrition Tracker Web App

A modern, user-friendly web application for tracking nutritional intake with personalized goals and recipe management.

## Features

### 🎯 Personal Goal Setting
- Set personalized nutrition goals (bulk, cut, or track nutrients)
- Input personal information (name, age, gender, height, weight)
- Create a customizable avatar with various appearance options

### 📱 Modern User Interface
- Beautiful gradient design with smooth animations
- Responsive layout that works on all devices
- Intuitive navigation with clear visual hierarchy

### 📊 Food Diary
- Track daily meals with detailed nutritional information
- View daily summaries with calories, protein, carbs, and fat
- Add and edit meals with ease
- Historical data tracking

### 👨‍🍳 Recipe Management
- **Personal Recipes**: Store and manage your favorite recipes
- **Friends' Recipes**: Discover and save recipes shared by friends
- Detailed nutritional information for each recipe
- Like and save recipes for quick access

### 🎨 Avatar Customization
- Customize hair color, eye color, and skin tone
- Similar to popular apps like Duolingo and Snapchat
- Visual representation of your profile

## Getting Started

### Prerequisites
- Node.js (version 14 or higher)
- npm or yarn package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd nutrition-tracker
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open your browser and navigate to `http://localhost:3000`

### Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Ejects from Create React App (one-way operation)

## Technology Stack

- **Frontend**: React 18 with TypeScript
- **Styling**: Styled Components
- **Icons**: Lucide React
- **Build Tool**: Create React App
- **Package Manager**: npm

## Project Structure

```
src/
├── components/          # React components
│   ├── Onboarding.tsx   # User registration and avatar creation
│   ├── MainMenu.tsx     # Main navigation interface
│   ├── FoodDiary.tsx    # Food tracking and diary
│   └── Recipes.tsx      # Recipe management
├── types/               # TypeScript type definitions
│   └── index.ts
├── App.tsx              # Main application component
└── index.tsx            # Application entry point
```

## Features in Detail

### Onboarding Process
1. **Personal Information**: Enter name, age, gender, height, weight
2. **Goal Selection**: Choose between bulk, cut, or nutrient tracking
3. **Avatar Creation**: Customize appearance with various options

### Main Menu
- **Top Panel**: Personalized greeting with user's avatar
- **Navigation Buttons**: Three main sections (Diary, Personal Recipes, Friends' Recipes)
- **Responsive Design**: Adapts to different screen sizes

### Food Diary
- **Daily Entries**: Organized by date with clear sections
- **Meal Tracking**: Add multiple meals per day (Breakfast, Lunch, etc.)
- **Nutritional Data**: Detailed breakdown of calories, protein, carbs, and fat
- **Daily Summaries**: Quick overview of daily nutritional intake

### Recipe Management
- **Personal Recipes**: Create and manage your own recipe collection
- **Friends' Recipes**: Browse and save recipes from friends
- **Recipe Details**: View ingredients, instructions, and nutritional information
- **Like System**: Save favorite recipes for quick access

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the GitHub repository. 