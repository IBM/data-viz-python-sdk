import React, { useContext, useCallback } from 'react';
import fileSize from 'filesize';
import moment from 'moment';
import { chain } from 'lodash';

import {
  FileUploaderItem,
  StructuredListWrapper,
  StructuredListHead,
  StructuredListBody,
  StructuredListRow,
  StructuredListCell,
} from 'carbon-components-react';

import DataContext from './context-data';

const Review = () => {
  const { file, selectedData } = useContext(DataContext),
    COMPONENT_NAME = 'pages-review';

  const getDetail = (label, value) => {
    return (
      <div className={`${COMPONENT_NAME}-file-data-item`}>
        <div className={'bx--label'}>{label}</div>
        <div>{value}</div>
      </div>
    );
  }

  const getFileDetails = useCallback(() => {
    return file && (
      <div className={`${COMPONENT_NAME}-file-data-wrapper`}>
        {getDetail('File Size', fileSize(file.size))}
        {getDetail('Last Modified', moment(file.lastModified).format('LLL'))}
      </div>
    );
  }, [file]);

  const getRowData = () => {
    const data = chain(selectedData)
      .values()
      .orderBy(['index'])
      .map(item => (
        <StructuredListRow key={`row-${item.id}`}>
          <StructuredListCell>{item.name}</StructuredListCell>
          <StructuredListCell>{item.type}</StructuredListCell>
        </StructuredListRow>
      ))
      .value();
    return data;
  }

  return (
    <div className={`${COMPONENT_NAME} bx--row`}>
      <div className={'bx--col-lg-12'}>
        <div className={`${COMPONENT_NAME}-subheading`}>{'File Details'}</div>
        <div className={`${COMPONENT_NAME}-details`}>
          <FileUploaderItem
            name={file.name}
            status={'complete'}
          />
          {getFileDetails()}
        </div>
        <hr />
        <div className={`${COMPONENT_NAME}-details`}>
          <StructuredListWrapper>
            <StructuredListHead>
              <StructuredListRow head>
                <StructuredListCell head>{'Column Name'}</StructuredListCell>
                <StructuredListCell head>{'Data Type'}</StructuredListCell>
              </StructuredListRow>
            </StructuredListHead>
            <StructuredListBody>
              {getRowData()}
            </StructuredListBody>
          </StructuredListWrapper>
        </div>
      </div>
    </div>
  );
};

export default Review;
