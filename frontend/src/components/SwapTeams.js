import React, { Fragment, useState } from 'react';
//useState https://reactjs.org/docs/hooks-state.html

const SwapTeams = () => {
	const [teamDescriptions, setTeamDescriptions] = useState([]);


	let response = ['apple','bob']
	let teamOne; 
	//console.log(firstTeam);

	const firstTeam = (name) => {
		teamOne = name;
		console.log(teamOne);
	}

	return(
		<Fragment>
			<h2 className='text-center'>Swap Teams To View Simulated Standings</h2>
			    <div className="row">

    		  		<div className="col-sm text-center">
						<h3>Team to swap out</h3>
							<div className="dropdown">
								<button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							    	Select Team
							 	</button>
								<div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
							    	<a className="dropdown-item" href="#">Atlanta Hawks</a>
							    	<a className="dropdown-item" href="#">Boston Celtics</a>
							    	<a className="dropdown-item" href="#">Brooklyn Nets</a>
							    	<a className="dropdown-item" href="#">Charlotte Hornets</a>
							    	<a className="dropdown-item" href="#">Chicago Bulls</a>
							    	<a className="dropdown-item" href="#">Cleveland Cavaliers</a>
							    	<a className="dropdown-item" href="#">Dallas Mavericks</a>
							    	<a className="dropdown-item" href="#">Denver Nuggets</a>
							    	<a className="dropdown-item" href="#">Golden State Warriors</a>
							    	<a className="dropdown-item" href="#">Houston Rockets</a>
							    	<a className="dropdown-item" href="#">Indiana Pacers</a>
							    	<a className="dropdown-item" href="#">LA Clippers</a>
							    	<a className="dropdown-item" href="#">LA Lakers</a>
							    	<a className="dropdown-item" href="#">Memphis Grizzlies</a>
							    	<a className="dropdown-item" href="#">Miami Heat</a>
							    	<a className="dropdown-item" href="#">Milwaukee Bucks</a>
							    	<a className="dropdown-item" href="#">Minnesota Timberwolves</a>
							    	<a className="dropdown-item" href="#">New Orleans Hornets</a>
							    	<a className="dropdown-item" href="#">New York Knicks</a>
							    	<a className="dropdown-item" href="#">Oklahoma City Thunder</a>
							    	<a className="dropdown-item" href="#">Orlando Magic</a>
							    	<a className="dropdown-item" href="#">Philadelphia Sixers</a>
							    	<a className="dropdown-item" href="#">Phoenix Suns</a>
							    	<a className="dropdown-item" href="#">Portland Trail Blazers</a>
							    	<a className="dropdown-item" href="#">Sacramento Kings</a>
							    	<a className="dropdown-item" href="#">San Antonio Spurs</a>
							    	<a className="dropdown-item" href="#">Toronto Raptors</a>
							    	<a className="dropdown-item" href="#">Utah Jazz</a>
							    	<a className="dropdown-item" href="#">Washington Wizards</a>
								</div>
							</div>

							<div className="dropdown mt-3">
								<button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							    	Select Year
							 	</button>
								<div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
							    	<a className="dropdown-item" href="#">2019-20</a>
							    	<a className="dropdown-item" href="#">2018-19</a>
							    	<a className="dropdown-item" href="#">2017-18</a>
							    	<a className="dropdown-item" href="#">2016-17</a>
							    	<a className="dropdown-item" href="#">2015-16</a>
							    	<a className="dropdown-item" href="#">2014-15</a>
								</div>	
							</div>
					</div>

					<div className="col-sm text-center">
						<h3>Team to swap in</h3>
							<div className="dropdown">
								<button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							    	Select Team
							 	</button>
								<div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
							    	<a className="dropdown-item" href="#">Atlanta Hawks</a>
							    	<a className="dropdown-item" href="#">Boston Celtics</a>
							    	<a className="dropdown-item" href="#">Brooklyn Nets</a>
							    	<a className="dropdown-item" href="#">Charlotte Hornets</a>
							    	<a className="dropdown-item" href="#">Chicago Bulls</a>
							    	<a className="dropdown-item" href="#">Cleveland Cavaliers</a>
							    	<a className="dropdown-item" href="#">Dallas Mavericks</a>
							    	<a className="dropdown-item" href="#">Denver Nuggets</a>
							    	<a className="dropdown-item" href="#">Golden State Warriors</a>
							    	<a className="dropdown-item" href="#">Houston Rockets</a>
							    	<a className="dropdown-item" href="#">Indiana Pacers</a>
							    	<a className="dropdown-item" href="#">LA Clippers</a>
							    	<a className="dropdown-item" href="#">LA Lakers</a>
							    	<a className="dropdown-item" href="#">Memphis Grizzlies</a>
							    	<a className="dropdown-item" href="#">Miami Heat</a>
							    	<a className="dropdown-item" href="#">Milwaukee Bucks</a>
							    	<a className="dropdown-item" href="#">Minnesota Timberwolves</a>
							    	<a className="dropdown-item" href="#">New Orleans Hornets</a>
							    	<a className="dropdown-item" href="#">New York Knicks</a>
							    	<a className="dropdown-item" href="#">Oklahoma City Thunder</a>
							    	<a className="dropdown-item" href="#">Orlando Magic</a>
							    	<a className="dropdown-item" href="#">Philadelphia Sixers</a>
							    	<a className="dropdown-item" href="#">Phoenix Suns</a>
							    	<a className="dropdown-item" href="#">Portland Trail Blazers</a>
							    	<a className="dropdown-item" href="#">Sacramento Kings</a>
							    	<a className="dropdown-item" href="#">San Antonio Spurs</a>
							    	<a className="dropdown-item" href="#">Toronto Raptors</a>
							    	<a className="dropdown-item" href="#">Utah Jazz</a>
							    	<a className="dropdown-item" href="#">Washington Wizards</a>
								</div>
							</div>

							<div className="dropdown mt-3">
								<button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							    	Select Year
							 	</button>
								<div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
							    	<a className="dropdown-item" href="#">2019-20</a>
							    	<a className="dropdown-item" href="#">2018-19</a>
							    	<a className="dropdown-item" href="#">2017-18</a>
							    	<a className="dropdown-item" href="#">2016-17</a>
							    	<a className="dropdown-item" href="#">2015-16</a>
							    	<a className="dropdown-item" href="#">2014-15</a>
								</div>	
							</div>

					</div>
				</div>

		</Fragment>
	); 

};

export default SwapTeams;

/*  
							<div className="dropdown">
								<button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
							    	Select Team dsadasdasdasd
							 	</button>
								<div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
							    	<a className="dropdown-item" href="#">Action</a>
							    	<a className="dropdown-item" href="#">Another action</a>
							    	<a className="dropdown-item" href="#">Something else here</a>
								</div>
							</div>

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