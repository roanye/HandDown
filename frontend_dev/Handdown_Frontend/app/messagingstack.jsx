import React, { useState } from 'react';
import Messaging from './messaginghome';
import Conversation from './individualmessage';

const MessagingFunctionality = () => {
    const [screen, setScreen] = useState('MessagingHome');
    const [routeParams, setRouteParams] = useState(null);
  
    const navigateToConversation = (params) => {
      setRouteParams(params);
      setScreen('Conversation');
    };
  
    const navigateBack = () => {
      setScreen('MessagingHome');
    };
  
    return (
      <>
        {screen === 'MessagingHome' ? (
          <Messaging navigateToConversation={navigateToConversation} />
        ) : (
          <Conversation route={{ params: routeParams }} navigateBack={navigateBack} />
        )}
      </>
    );
  };

export default MessagingFunctionality;
