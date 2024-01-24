import React, { useState } from "react";


const UrlShortenForm = () => {
	const [input_url, setInput_url] = useState("");
	const [shortened_url, setShortened_url] = useState("");
	/*const [input_hours, setInput_hours] = useState("");
	const [exp_time, setExp_time] = useState("");*/

	const handleSubmit = async(e) => {
		e.preventDefault();
		console.log("Url Submitted!");
		try{
			const response = await fetch("http://3.104.217.148:5000/shorten", {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({input_url})//, input_hours})
			});
			console.log("Calling API.");
			const data = await response.json();
			console.log(data);
			setShortened_url(data.Short_URL);
			//setExp_time(data.Exp_Time);
		}catch(error){
			console.error("Error: ", error);
		}
	};
	return (
		<div className="url-shorten-web">
			<h2>URL Shortener</h2>
			<form className="url-shorten-form" onSubmit={handleSubmit}>
          
				<input autoFocus value={input_url} placeholder="Long URL goes here." type="text" onChange={(e) => setInput_url(e.target.value)} />

				<button type="submit">Submit</button>
			</form>
			{shortened_url && (
				<div className="shortened-url">
					<h3>Shortened URL:</h3>
					<a href={shortened_url} target="_blank" rel="noopener noreferrer">{shortened_url}</a>
				</div>
			)}
		</div>
	);
};

export default UrlShortenForm;
