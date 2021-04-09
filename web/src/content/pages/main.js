import React, { useState } from 'react';
import { ProgressIndicator, ProgressStep, Loading } from 'carbon-components-react';

import DataContext from './context-data';

import Welcome from './welcome';
import AttachFile from './attach-file';
import DataSelection from './data-selection';
import Review from './review';
import Results from './results';
import Buttons from './buttons';

const Main = () => {
    const PANELS = {
        WELCOME: 0,
        ATTACH: 1,
        SELECTION: 2,
        REVIEW: 3,
        RESULTS: 4,
    };
    const COMPONENT_NAME = 'main-page';

    const [currentIndex, setCurrentIndex] = useState(PANELS.WELCOME),
        [file, setFile] = useState(),
        [disableNext, setDisableNext] = useState(false),
        [selectedColumns, setSelectedColumns] = useState({}),
        [selectedRows, setSelectedRows] = useState([]),
        [selectedData, setSelectedData] = useState([]),
        [isFetching, setFetching] = useState(false),
        [responseData, setResponseData] = useState();

    const getPanel = () => {
        return {
            [PANELS.WELCOME]: <Welcome />,
            [PANELS.ATTACH]: <AttachFile />,
            [PANELS.SELECTION]: <DataSelection />,
            [PANELS.REVIEW]: <Review />,
            [PANELS.RESULTS]: <Results />
        }[currentIndex];
    }

    const isPanelDisabled = (id) => currentIndex < id;

    return (
        <div className={COMPONENT_NAME}>
            <div className={`${COMPONENT_NAME}-title`}>{'Amhairc'}</div>
            <div className={`${COMPONENT_NAME}-container`}>
                <Loading active={isFetching} withOverlay={true} />
                <DataContext.Provider value={{
                    PANELS,
                    currentIndex, setCurrentIndex,
                    file, setFile,
                    selectedColumns, setSelectedColumns,
                    selectedRows, setSelectedRows,
                    selectedData, setSelectedData,
                    disableNext, setDisableNext,
                    isFetching, setFetching,
                    responseData, setResponseData
                }}>
                    <ProgressIndicator
                        currentIndex={currentIndex}
                        spaceEqually
                        onChange={setCurrentIndex}
                    >
                        <ProgressStep label={'Overview'}></ProgressStep>
                        <ProgressStep disabled={isPanelDisabled(PANELS.ATTACH)} label={'Attach'}></ProgressStep>
                        <ProgressStep disabled={isPanelDisabled(PANELS.SELECTION)} label={'Select Columns'}></ProgressStep>
                        <ProgressStep disabled={isPanelDisabled(PANELS.REVIEW)} label={'Review'}></ProgressStep>
                        <ProgressStep disabled={isPanelDisabled(PANELS.RESULTS)} label={'Results'}></ProgressStep>
                    </ProgressIndicator>
                    {getPanel()}
                    <Buttons />
                </DataContext.Provider>
            </div>
        </div>
    );
};

export default Main;
