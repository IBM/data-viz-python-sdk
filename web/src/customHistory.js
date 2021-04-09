import { createBrowserHistory } from 'history';

const contextRoot = '/';
const customHistory = createBrowserHistory({
  basename: contextRoot
});

export default customHistory;