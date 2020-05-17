import React, { Fragment, useState } from 'react';
//useState https://reactjs.org/docs/hooks-state.html

const SwapTeams = () => {
	const [teamDescriptions, setTeamDescriptions] = useState([]);

	return(
		<Fragment>
			<h2 className='text-center'>Swap Teams To View Simulated Standings</h2>
			    <div className="row">
    		  		<div className="col-sm text-center">
						<h3>Team to swap out</h3>
							<div className="dropdown">
							  <button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							    Dropdown button
							  </button>
							  <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
							    <a className="dropdown-item" href="#">Action</a>
							    <a className="dropdown-item" href="#">Another action</a>
							    <a className="dropdown-item" href="#">Something else here</a>
							  </div>
							</div>
					</div>
					<div className="col-sm text-center">
						<h3>Team to swap in</h3>
					</div>
				</div>

		</Fragment>
	); 

};

export default SwapTeams;

/*  

const InputTodo = () => {
	const [description, setDescription] = useState(''); //you can use hooks instead of classes

	const onSubmitForm = async e => {
		e.preventDefault(); //prevent refresh
		try {
			const body = { description };
			const response = await fetch('http://localhost:5000/todos',{ //Wait for it to finish then consolelog response
				method: 'POST',
				headers: { 'Content-Type': 'application/json'},
				body: JSON.stringify(body)
			}); // by default fetch is a get request

			//console.log(response);
			window.location = '/'; //Once response is sent it will refresh and show the changes
		}catch (err) {
			console.error(err.message);
		}
	}

	//onSubmit is a DOM event
	return (
		<Fragment>
			<h1 className='text-center mt-5'>Pern Todo List</h1>
			<form className='d-flex mt-5' onSubmit={ onSubmitForm }> 
				<input type='text' className='form-control' value={description} onChange={e => setDescription(e.target.value)}/>
				<button className='btn btn-success'>Add</button>
			</form>
		</Fragment>
	);

*/