import React, { useContext, useEffect } from 'react';
import ReactIframe from '@jschaftenaar/react-iframe';
import { values, now, get, isEmpty } from 'lodash';

import ErrorWidget from '../wrappers/error-widget';
import EmptyWidget from '../wrappers/empty-widget';

import request from '../utils/request';
import customHistory from '../../customHistory';

import DataContext from './context-data';

const Results = () => {
  const {
    responseData, setResponseData,
    file, selectedData,
    isFetching, setFetching,
  } = useContext(DataContext),
    COMPONENT_NAME = 'pages-results';


  useEffect(() => {

    const data = values(selectedData);
    const formData = new FormData();

    formData.append('file', file);
    formData.append('data', JSON.stringify(data));

    request.uploadData(formData)
      .then(response => {
        const { status, statusText } = response;
        response.json().then((data) => {
          setResponseData({ status, statusText, ...data });
          setFetching(false);
        });
      })
  }, []);

  const getLoader = () => '"data:image/svg+xml, %3Csvg width=\'130px\' height=\'130px\' xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\' preserveAspectRatio=\'xMidYMid\' %3E%3Ccircle cx=\'50\' cy=\'50\' fill=\'none\' stroke=\'%230F62FE\' stroke-width=\'9\' r=\'45\' stroke-dasharray=\'212.05750411731105 72.68583470577035\' transform=\'rotate(143.505 50 50)\' %3E%3CanimateTransform attributeName=\'transform\' type=\'rotate\' calcMode=\'linear\' values=\'0 50 50;360 50 50\' keyTimes=\'0;1\' dur=\'0.5s\' begin=\'0s\' repeatCount=\'indefinite\' %3E%3C/animateTransform%3E%3C/circle%3E%3C/svg%3E"';

  const getEmpty = () => {
    return (
      <EmptyWidget
        heading={'Oops... Something is missing'}
        subText={'No chart path found'}
      />
    );
  }

  const getError = () => {
    return (
      <ErrorWidget
        status={responseData.status}
        statusText={responseData.statusText}
        error={responseData.error}
      />
    );
  }

  const mainComponent = () => {

    if (isFetching) {
      return;
    }

    if (get(responseData, 'error')) {
      return getError();
    }

    const chartPath = get(responseData, 'path');

    if (isEmpty(chartPath)) {
      return getEmpty();
    }

    return (
      <ReactIframe
        message={{ procedure: now(), arguments: now() }}
        src={`http://localhost${chartPath}`}
        scrolling={true}
        loader={getLoader()}
      />
    );

    // JSON.stringify(responseData, null, '\t');
  }

  return (
    <div className={`${COMPONENT_NAME}`}>
      {mainComponent()}
    </div>
  );
};

export default Results;
