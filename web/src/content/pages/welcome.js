import React, { useEffect, useContext } from 'react';

import DataContext from './context-data';

const Welcome = () => {
  const { setDisableNext } = useContext(DataContext);

  useEffect(() => {
    setDisableNext(false);
  }, []);

  return (
    <div className={'App'}>
      <header className={'App-header'}>
          <div className={'App-body'}>
            <img src="Glendalough.jpg" width="400px" alt="amhairc"/>
            <p id="para">Amhairc means "visual" in Irish, the name given to our Data Visualisation Charting best practice library.
                Sometimes visual image can be understood and interpreted quickly and easily. For example the picture above
                of Glendalough in Wicklow, Ireland is stunning but that opinion is subjective.
                Creating charts using data visualisations best practice is an objective process with a right and wrong way to do create them.
                This is based on research that encompasses colors, sizing, placement and the way in which the human mind interprets visually represented data.
                We hope to show you how this works in practice with our simple web app.
            </p>
          </div>
        </header>
      </div>
  );
}

export default Welcome;