import React, { useState } from 'react';
import { User } from './types';
import Onboarding from './components/Onboarding';
import MainMenu from './components/MainMenu';
import FoodDiary from './components/FoodDiary';
import Recipes from './components/Recipes';

type Page = 'onboarding' | 'main' | 'diary' | 'personal-recipes' | 'friends-recipes';

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<Page>('onboarding');
  const [user, setUser] = useState<User | null>(null);

  const handleOnboardingComplete = (userData: User) => {
    setUser(userData);
    setCurrentPage('main');
  };

  const handleNavigation = (page: string) => {
    setCurrentPage(page as Page);
  };

  const handleBackToMain = () => {
    setCurrentPage('main');
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'onboarding':
        return <Onboarding onComplete={handleOnboardingComplete} />;
      
      case 'main':
        return user ? (
          <MainMenu user={user} onNavigate={handleNavigation} />
        ) : null;
      
      case 'diary':
        return <FoodDiary onBack={handleBackToMain} />;
      
      case 'personal-recipes':
        return <Recipes onBack={handleBackToMain} type="personal" />;
      
      case 'friends-recipes':
        return <Recipes onBack={handleBackToMain} type="friends" />;
      
      default:
        return <Onboarding onComplete={handleOnboardingComplete} />;
    }
  };

  return (
    <div className="App">
      {renderCurrentPage()}
    </div>
  );
};

export default App; 