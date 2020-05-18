import React, { Fragment, useState } from 'react';
//useState https://reactjs.org/docs/hooks-state.html

const SwapTeams = () => {
	const [teamDescriptions, setTeamDescriptions] = useState([
		{
			teamName: 'Atlanta Hawks',
			wins: 82,
			losses: 0,
			wlPercent: '100%'
		},
		{
			teamName: 'Boston Celtics',
			wins: 81,
			losses: 1,
			wlPercent: '99%'
		},
		{
			teamName: 'Brooklyn Nets',
			wins: 80,
			losses: 2,
			wlPercent: '98%'
		},
		{
			teamName: 'Charlotte Hornets',
			wins: 79,
			losses: 3,
			wlPercent: '97%'
		},
		{
			teamName: 'Chicago Bulls',
			wins: 78,
			losses: 4,
			wlPercent: '96%'
		},
	]);
		

	let teamList = ['Atlanta Hawks','2019-20','Atlanta Hawks','2019-20']

	let response = ['apple','bob']
	let teamOne; 
	//console.log(firstTeam);

	const firstTeam = (name) => {
		teamOne = name;
		console.log(teamOne);
	}
	/*
			const response = await fetch('http://localhost:5000/todos',{ //Wait for it to finish then consolelog response
				method: 'POST',
				headers: { 'Content-Type': 'application/json'},
				body: JSON.stringify(body)
			}); // by default fetch is a get request
	*/
	const onSubmitForm = async e => {
		e.preventDefault();
		//console.log('teamDescriptions',teamDescriptions);
		//console.log('teamList', teamList);
		const body = { teamList: teamList };

		const response = await fetch('/standings',{
			method: 'POST',
			headers: { 'Content-Type': 'application/json'},
			body: JSON.stringify(body)
		});
		const jsonData = await response.json();

		console.log('jsondata',jsonData);

		//setTeamDescriptions(teamDescriptions+1);
	}

	return(
		<Fragment>
			<h2 className='text-center'>Swap Teams To View Simulated Standings</h2>
		    <form  onSubmit={ onSubmitForm }>
			    <div className="row">
    		  		<div className="col-sm text-center">
						<h3>Team to swap out</h3>
							<select onChange={e => teamList[0]=(e.target.value)}>
							  <option value="Atlanta Hawks">Atlanta Hawks</option>
							  <option value="Boston Celtics">Boston Celtics</option>
							  <option value="Brooklyn Nets">Brooklyn Nets</option>
							  <option value="Charlotte Hornets">Charlotte Hornets</option>
							  <option value="Chicago Bulls">Chicago Bulls</option>
							  <option value="Cleveland Cavaliers">Cleveland Cavaliers</option>
							  <option value="Dallas Mavericks">Dallas Mavericks</option>
							  <option value="Golden State Warriors">Golden State Warriors</option>
							  <option value="Houston Rockets">Houston Rockets</option>
							  <option value="Indiana Pacers">Indiana Pacers</option>
							  <option value="LA Clippers">LA Clippers</option>
							  <option value="LA Lakers">LA Lakers</option>
							  <option value="Memphis Grizzlies">Memphis Grizzlies</option>
							  <option value="Miami Heat">Miami Heat</option>
							  <option value="Milwaukee Bucks">Milwaukee Bucks</option>
							  <option value="Minnesota Timberwolves">Minnesota Timberwolves</option>
							  <option value="New Orleans Hornets">New Orleans Hornets</option>
							  <option value="New York Knicks">New York Knicks</option>
							  <option value="Oklahoma City Thunder">Oklahoma City Thunder</option>
							  <option value="Orlando Magic">Orlando Magic</option>
							  <option value="Philadelphia Sixers">Philadelphia Sixers</option>
							  <option value="Phoenix Suns">Phoenix Suns</option>
							  <option value="Portland Trail Blazers">Portland Trail Blazers</option>
							  <option value="Sacramento Kings">Sacramento Kings</option>
							  <option value="San Antonio Spurs">San Antonio Spurs</option>
							  <option value="Toronto Raptors">Toronto Raptors</option>
							  <option value="Utah Jazz">Utah Jazz</option>
							  <option value="Washington Wizards">Washington Wizards</option>
							</select>

							<select className="ml-1" onChange={e => teamList[1]=(e.target.value)}>
							    <option value="2019-20">2019-20</option>
							    <option value="2018-19">2018-19</option>
							    <option value="2017-18">2017-18</option>
							    <option value="2016-17">2016-17</option>
							    <option value="2015-16">2015-16</option>
							    <option value="2014-15">2014-15</option>
							</select>
					</div>

    		  		<div className="col-sm text-center">
						<h3>Team to swap in</h3>
							<select onChange={e => teamList[2]=(e.target.value)}>
							  <option value="Atlanta Hawks">Atlanta Hawks</option>
							  <option value="Boston Celtics">Boston Celtics</option>
							  <option value="Brooklyn Nets">Brooklyn Nets</option>
							  <option value="Charlotte Hornets">Charlotte Hornets</option>
							  <option value="Chicago Bulls">Chicago Bulls</option>
							  <option value="Cleveland Cavaliers">Cleveland Cavaliers</option>
							  <option value="Dallas Mavericks">Dallas Mavericks</option>
							  <option value="Golden State Warriors">Golden State Warriors</option>
							  <option value="Houston Rockets">Houston Rockets</option>
							  <option value="Indiana Pacers">Indiana Pacers</option>
							  <option value="LA Clippers">LA Clippers</option>
							  <option value="LA Lakers">LA Lakers</option>
							  <option value="Memphis Grizzlies">Memphis Grizzlies</option>
							  <option value="Miami Heat">Miami Heat</option>
							  <option value="Milwaukee Bucks">Milwaukee Bucks</option>
							  <option value="Minnesota Timberwolves">Minnesota Timberwolves</option>
							  <option value="New Orleans Hornets">New Orleans Hornets</option>
							  <option value="New York Knicks">New York Knicks</option>
							  <option value="Oklahoma City Thunder">Oklahoma City Thunder</option>
							  <option value="Orlando Magic">Orlando Magic</option>
							  <option value="Philadelphia Sixers">Philadelphia Sixers</option>
							  <option value="Phoenix Suns">Phoenix Suns</option>
							  <option value="Portland Trail Blazers">Portland Trail Blazers</option>
							  <option value="Sacramento Kings">Sacramento Kings</option>
							  <option value="San Antonio Spurs">San Antonio Spurs</option>
							  <option value="Toronto Raptors">Toronto Raptors</option>
							  <option value="Utah Jazz">Utah Jazz</option>
							  <option value="Washington Wizards">Washington Wizards</option>
							</select>

							<select className="ml-1"  onChange={e => teamList[3]=(e.target.value)}>
							    <option value="2019-20">2019-20</option>
							    <option value="2018-19">2018-19</option>
							    <option value="2017-18">2017-18</option>
							    <option value="2016-17">2016-17</option>
							    <option value="2015-16">2015-16</option>
							    <option value="2014-15">2014-15</option>
							</select>
					</div>

				</div>
				<div className="row justify-content-center">
				    <button type="submit" className="btn btn-primary">Submit</button>
				</div>
			</form>

			<h2 className='text-center'>Standings</h2>
			<p>Counter {teamDescriptions[0].teamName}</p>
			<table class="table table-striped">
			    <thead>
			    	<tr>
			        	<th>Team Name</th>
			        	<th>Wins</th>
			        	<th>Losses</th>
			        	<th>Win/Loss PCT</th>
			    	</tr>
			    </thead>
			    <tbody>
			    	<tr>
			    	  <td>John</td>
			    	  <td>Doe</td>
			    	  <td>john@example.com</td>
			    	</tr>
			    	<tr>
			    	  <td>Mary</td>
			    	  <td>Moe</td>
			    	  <td>mary@example.com</td>
			    	</tr>
			    	<tr>
			    	  <td>July</td>
			    	  <td>Dooley</td>
			    	  <td>july@example.com</td>
			    	</tr>
			    </tbody>
			</table>
		</Fragment>
	); 

};

export default SwapTeams;

/*  


Previous Code:
// --------------- DROP DOWN ------
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


---------------------------  REFERENCE: 

Selection Menu
https://getbootstrap.com/docs/4.0/components/forms/#select-menu

<select class="custom-select">
  <option selected>Open this select menu</option>
  <option value="1">One</option>
  <option value="2">Two</option>
  <option value="3">Three</option>
</select>

*/