import React from 'react';
import styled from 'styled-components';
import { User } from '../types';
import { BookOpen, ChefHat, Users } from 'lucide-react';

interface MainMenuProps {
  user: User;
  onNavigate: (page: string) => void;
}

const MainContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
`;

const TopPanel = styled.div`
  background: white;
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
`;

const Greeting = styled.h1`
  color: #333;
  font-size: 2.5rem;
  margin-bottom: 20px;
  font-weight: 600;
`;

const AvatarContainer = styled.div`
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin: 0 auto 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  border: 6px solid white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
`;

const NavigationButtons = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 30px;
`;

const NavButton = styled.button`
  background: white;
  border-radius: 15px;
  padding: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 2px solid transparent;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    border-color: #667eea;
  }
`;

const IconContainer = styled.div`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
`;

const ButtonTitle = styled.h3`
  font-size: 1.5rem;
  color: #333;
  font-weight: 600;
  margin: 0;
`;

const ButtonDescription = styled.p`
  color: #666;
  text-align: center;
  margin: 0;
  line-height: 1.5;
`;

const MainMenu: React.FC<MainMenuProps> = ({ user, onNavigate }) => {
  return (
    <MainContainer>
      <TopPanel>
        <Greeting>Hi, {user.name}!</Greeting>
        <AvatarContainer>
          👤
        </AvatarContainer>
      </TopPanel>

      <NavigationButtons>
        <NavButton onClick={() => onNavigate('diary')}>
          <IconContainer>
            <BookOpen size={30} />
          </IconContainer>
          <ButtonTitle>My Diary</ButtonTitle>
          <ButtonDescription>
            Track your daily meals and nutritional intake
          </ButtonDescription>
        </NavButton>

        <NavButton onClick={() => onNavigate('personal-recipes')}>
          <IconContainer>
            <ChefHat size={30} />
          </IconContainer>
          <ButtonTitle>Personal Recipes</ButtonTitle>
          <ButtonDescription>
            Store and manage your favorite recipes
          </ButtonDescription>
        </NavButton>

        <NavButton onClick={() => onNavigate('friends-recipes')}>
          <IconContainer>
            <Users size={30} />
          </IconContainer>
          <ButtonTitle>Friends' Recipes</ButtonTitle>
          <ButtonDescription>
            Discover recipes shared by your friends
          </ButtonDescription>
        </NavButton>
      </NavigationButtons>
    </MainContainer>
  );
};

export default MainMenu; 