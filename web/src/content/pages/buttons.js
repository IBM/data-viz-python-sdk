import React, { useMemo, useContext } from 'react';
import { Button } from 'carbon-components-react';

import DataContext from './context-data';

const Buttons = () => {
  const {
    PANELS,
    disableNext,
    setFetching,
    currentIndex, setCurrentIndex
  } = useContext(DataContext);

  const hasSubmitButton = useMemo(() => {
    return (currentIndex === PANELS.REVIEW)
  }, [currentIndex]);

  const hasNextButton = useMemo(() => {
    return (currentIndex < PANELS.REVIEW);
  }, [currentIndex]);

  const hasPreviousButton = useMemo(() => {
    return (currentIndex > PANELS.WELCOME);
  }, [currentIndex]);

  const onSubmit = () => {
    setFetching(true);
    setCurrentIndex(PANELS.RESULTS);
  }

  const updateIndex = (index) => {
    setCurrentIndex(index)
  }

  return (
    <div className={'buttons-container'}>
      { hasPreviousButton && <Button onClick={() => updateIndex(currentIndex - 1)}>{'Previous'}</Button>}
      { hasNextButton && <Button disabled={disableNext} onClick={() => updateIndex(currentIndex + 1)}>{'Next'}</Button>}
      { hasSubmitButton && <Button onClick={onSubmit}>{'Start Charting'}</Button>}
    </div>
  );
};

export default Buttons;
