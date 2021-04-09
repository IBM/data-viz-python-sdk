import React, { useMemo } from 'react';

import errorSvg from '../images/error-state.svg';

import EmptyWidget from './empty-widget';

const COMPONENT_NAME = 'error-widget';

const ErrorWidget = ({ error, status, statusText }) => {
  const header = useMemo(() => {
    return (
      <div className={'error-header'}>
        {'Oops...'}
        { status && <span className={'error-code'}>{`[ Error ${status} ]`}</span>}
        {error || statusText}
      </div>
    )
  }, [error, status, statusText]);

  return (
    <EmptyWidget
      className={COMPONENT_NAME}
      image={errorSvg}
      heading={header}
    />
  );

};

export default ErrorWidget;
