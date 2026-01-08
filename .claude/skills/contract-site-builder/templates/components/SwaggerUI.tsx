import React from 'react';
import SwaggerUI from 'swagger-ui-react';
import 'swagger-ui-react/swagger-ui.css';

interface SwaggerUIComponentProps {
  specUrl: string;
}

export default function SwaggerUIComponent({ specUrl }: SwaggerUIComponentProps) {
  return (
    <div style={{ marginTop: '2rem' }}>
      <SwaggerUI url={specUrl} />
    </div>
  );
}
