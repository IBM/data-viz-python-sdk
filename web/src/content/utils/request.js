import fetch from 'isomorphic-fetch';


// const send = (url, options, timeout = 1) => {
//   return Promise.race([
//       fetch(url, options),
//       new Promise((_, reject) =>
//           setTimeout(() => reject(new Error('timeout')), timeout)
//       )
//   ]);
// }

export const uploadData = (data) => {
  return fetch('http://localhost/upload', {
    method: 'POST',
    credentials: 'include',
    body: data,
    timeout: 30000
  });
};

export default {
  uploadData
}