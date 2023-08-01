import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  max-width: 1200px;
  min-width: 350px;
  min-height: 100vh;
  margin: 0 auto;
  padding: 16px;
  /* border: 1px solid #ccc;*/
`;

const PageLayout = ({ children }) => {
    return (
      <Container>
        {children}
      </Container>
    );
  };

export default PageLayout;