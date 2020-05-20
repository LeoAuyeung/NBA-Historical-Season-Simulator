import React, { Fragment, useState } from 'react';

const SwapTeams = () => {
	const [predictions, setPredictions] = useState([]);

	let teamList = ["",'2018-19','Chicago Bulls','2015-16']

	const onSubmitForm = async e => {
		e.preventDefault();
		const body = { teamList: teamList };
		
		const response = await fetch('/standings',{
			method: 'POST',
			headers: { 'Content-Type': 'application/json'},
			body: JSON.stringify(body)
		});
		const jsonData = await response.json();


		setPredictions(jsonData.listOfPredictions)
	}

	return(
		<Fragment>
			<h2 className='text-center'>Swap Teams To View Simulated Standings</h2>
		    <form  onSubmit={ onSubmitForm }>
			    <div className="row">
    		  		<div className="col-sm text-center">
						<h3>Season To Play In</h3>


							<select className="ml-1" onChange={e => teamList[1]=(e.target.value)}>
							    <option selected value="2018-19">2018-19</option>
							    <option value="2017-18">2017-18</option>
							    <option value="2016-17">2016-17</option>
							    <option value="2015-16">2015-16</option>
							    <option value="2014-15">2014-15</option>
								<option value="2013-14">2013-14</option>
								<option value="2012-13">2012-13</option>
								<option value="2011-12">2011-12</option>
								<option value="2010-11">2010-11</option>
							</select>
					</div>

    		  		<div className="col-sm text-center">
						<h3>Team to swap in</h3>
							<select onChange={e => teamList[2]=(e.target.value)}>
							  <option value="Atlanta Hawks">Atlanta Hawks</option>
							  <option value="Boston Celtics">Boston Celtics</option>
							  <option value="Brooklyn Nets">Brooklyn Nets</option>
							  <option value="Charlotte Hornets">Charlotte Hornets</option>
							  <option selected value="Chicago Bulls">Chicago Bulls</option>
							  <option value="Cleveland Cavaliers">Cleveland Cavaliers</option>
							  <option value="Dallas Mavericks">Dallas Mavericks</option>
							  <option value="Golden State Warriors">Golden State Warriors</option>
							  <option value="Houston Rockets">Houston Rockets</option>
							  <option value="Indiana Pacers">Indiana Pacers</option>
							  <option value="Los Angeles Clippers">Los Angeles Clippers</option>
							  <option value="Los Angeles Lakers">Los Angeles Lakers</option>
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
								<option value="2018-19">2018-19</option>
							    <option value="2017-18">2017-18</option>
							    <option value="2016-17">2016-17</option>
							    <option selected value="2015-16">2015-16</option>
							    <option value="2014-15">2014-15</option>
								<option value="2013-14">2013-14</option>
								<option value="2012-13">2012-13</option>
								<option value="2011-12">2011-12</option>
								<option value="2010-11">2010-11</option>
							</select>
					</div>

				</div>
				<div className="row justify-content-center">
				    <button type="submit" className="btn btn-primary">Submit</button>
				</div>
			</form>

			<h2 className='text-center mt-4'>Predicted Games</h2>
			<table className="table table-striped">
			    <thead>
			    	<tr>
			        	<th>Home</th>
			        	<th>Away</th>
			        	<th>Prediction</th>
			    	</tr>
			    </thead>
			    <tbody>
			      	{predictions.map((game,index) => (
			      		<tr key={index} index={index}>
			      			<td>{game.home}</td>
			      			<td>{game.away}</td>
			      			<td>{game.prediction}</td>
			      		</tr>
			      	))}
			    </tbody>
			</table>

		</Fragment>
	); 

};

export default SwapTeams;