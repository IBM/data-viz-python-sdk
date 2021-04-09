import React, { useState, useEffect, useContext, useCallback } from 'react';
import { get } from 'lodash';
import moment from 'moment';
import fileSize from 'filesize';

import {
  FileUploader,
  FileUploaderDropContainer,
  FileUploaderItem
} from 'carbon-components-react';

import { MAX_FILE_SIZE, MAX_FILE_SIZE_TEXT } from '../../constants';

import DataContext from './context-data';

const Attach = () => {
  const { file, setFile, setDisableNext, setSelectedColumns, setSelectedRows, setSelectedData } = useContext(DataContext),
    [invalidFile, setInvalidFile] = useState(false),
    COMPONENT_NAME = 'pages-attach';

  const resetSelectData = () => {
    setSelectedColumns({});
    setSelectedRows([]);
    setSelectedData([]);
  }

  const updateFile = evt => {
    setFile(get(evt, 'target.files[0]'));
    resetSelectData();
  }

  const onAddFiles = (evt, data) => {
    setFile(get(data, 'addedFiles[0]'))
  }

  const getFileSize = ({ size }) => {
    return get(fileSize(file.size, { output: 'object', exponent: 2 }), 'value', 0);
  }

  useEffect(() => {
    setDisableNext(!file || invalidFile);
    if (!file || invalidFile) {
      resetSelectData();
    }
  }, [file, invalidFile])

  useEffect(() => {
    if (file) {
      setInvalidFile(getFileSize(file) > MAX_FILE_SIZE);
    }
  }, [file]);


  const getFileDetail = (label, value) => {
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
        {getFileDetail('File Size', fileSize(file.size))}
        {getFileDetail('Last Modified', moment(file.lastModified).format('LLL'))}
      </div>
    );
  }, [file]);

  return (
    <div className={COMPONENT_NAME}>
      <div className={`${COMPONENT_NAME}-body`}>
        <div className={`${COMPONENT_NAME}-file-uploader`}>
          <FileUploaderDropContainer
            labelText={`Drag and drop files here or click to ${file ? 'replace' : 'upload'}`}
            accept={['.csv']}
            multiple={false}
            onAddFiles={onAddFiles}
          />
          <div className={`${COMPONENT_NAME}-file-uploader-middle`}>{'OR'}</div>
          <FileUploader
            labelTitle={'Upload .CSV file'}
            labelDescription={`Max file size is ${MAX_FILE_SIZE_TEXT}. Only .csv files are supported.`}
            buttonLabel={file ? 'Replace file' : 'Add file'}
            accept={['.csv']}
            multiple={false}
            iconDescription={'Clear file'}
            filenameStatus={'edit'}
            onDelete={() => setFile()}
            onChange={updateFile}
          />
        </div>
        <div className={`${COMPONENT_NAME}-file-item`}>
          {file &&
            <div className={`${COMPONENT_NAME}-file-data`}>
              <FileUploaderItem
                name={file.name}
                status={'edit'}
                iconDescription={'Clear file'}
                invalid={invalidFile}
                errorSubject={`File size exceeds limit`}
                errorBody={`${MAX_FILE_SIZE_TEXT} max file size. Select a new file and try again.`}
                onDelete={() => setFile()}
              />
              {getFileDetails()}
            </div>
          }
        </div>
      </div>
    </div>
  );
}

export default Attach;