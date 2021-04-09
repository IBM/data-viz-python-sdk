import { Route, Switch } from 'react-router-dom';
import { Link } from 'react-router-dom';

import Main from './content/pages/main';

function App() {
  return (
      <div element={Link} to="/">
          <Switch>
            <Route exact path="/*" component={Main} />
          </Switch>
      </div>
  );
}

export default App;

