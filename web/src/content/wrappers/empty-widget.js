import React from 'react';

import notFoundSvg from '../images/not-found.svg';

const COMPONENT_NAME = 'empty-widget';


const EmptyState = ({ className, caption, heading, subText, image }) => {
  return (
    <div className={(className || COMPONENT_NAME)}>
      <div className={`${COMPONENT_NAME}-full`}>
        <img alt='' className={`${COMPONENT_NAME}__svg`} src={(image || notFoundSvg)}/>
        <div className={`${COMPONENT_NAME}-details`}>
          <div className={`${COMPONENT_NAME}-heading`}>{ heading }</div>
          { subText && <p id='empty-subtext'>{subText}</p> }
        </div>
      </div>
    </div>
  );

};

export default EmptyState;
