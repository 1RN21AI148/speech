const apiJson = {
  getApi: {
      url: '/',
      method: 'GET',
      headers: {
        'Accept': '*/*',
      }, 
  },
  getSongs: {
    url: '/getsongs',
    method: 'GET',
    headers: {
      'Accept': '*/*',
    }, 
  },
  addSong: {
    url: '/addsong',
    method: 'POST',
    headers: {
      'Accept': '*/*',
      'Content-Type': 'application/json',
    }, 
  },
}

export default apiJson;