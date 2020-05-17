import React, { useState, useEffect, Fragment } from 'react';

//components
import SwapTeams from './components/SwapTeams';


function App() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <Fragment>
      <div className = 'container'>
        <h1 className='text-center mt-5'>NBA Historical Season Simulator</h1>
        <SwapTeams />
        <p className='text-center'>API Call Tester {currentTime}.</p>
      </div>
    </Fragment>
  );
}

export default App;