export interface User {
  name: string;
  age: number;
  gender: 'male' | 'female' | 'other';
  height: number;
  weight: number;
  goal: 'bulk' | 'cut' | 'track';
  avatar: Avatar;
}

export interface Avatar {
  hairColor: string;
  hairStyle: string;
  eyeColor: string;
  skinTone: string;
  accessories: string[];
}

export interface Food {
  id: string;
  name: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  fiber: number;
  sugar: number;
  sodium: number;
}

export interface Meal {
  id: string;
  name: string;
  foods: Food[];
  totalCalories: number;
  totalProtein: number;
  totalCarbs: number;
  totalFat: number;
}

export interface DailyEntry {
  date: string;
  meals: Meal[];
  totalCalories: number;
  totalProtein: number;
  totalCarbs: number;
  totalFat: number;
}

export interface Recipe {
  id: string;
  name: string;
  ingredients: Food[];
  instructions: string[];
  prepTime: number;
  cookTime: number;
  servings: number;
  isPersonal: boolean;
  author?: string;
} 