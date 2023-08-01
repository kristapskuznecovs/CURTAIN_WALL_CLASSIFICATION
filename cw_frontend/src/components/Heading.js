import React from 'react';
import styled from 'styled-components';

const HeadingContainer = styled.div`
  text-align: left;   
  margin-bottom: 16px
  margin-bottom: 16px
`;

const HeadingText = styled.h1`
  font-size: 24px;
  color: #333;
  white-space: nowrap;
`;

const Heading = ({ children }) => {
  return (
    <HeadingContainer>
        <HeadingText>{children}</HeadingText>
    </HeadingContainer>
  );
};

export default Heading;