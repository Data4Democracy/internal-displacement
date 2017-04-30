import React from 'react';
import { Link } from 'react-router';
import {Element} from 'react-scroll';

import pic1 from './../../themeCss/images/pic01.jpg';
import pic2 from './../../themeCss/images/pic02.jpg';
import pic3 from './../../themeCss/images/pic03.jpg';
import pic4 from './../../themeCss/images/pic04.jpg';

const HomePage = () => (
	<div id="homePage">
		<section id="banner">
			<div className="inner">
				<h2>Internal Displacement</h2>
				<p>A Data for Democracy solution for the Unite Ideas IDETECT Challenge.</p>
				<ul className="actions">
				</ul>
			</div>
			<a href="#one" className="more scrolly">Learn More</a>
		</section>

        <section id="one" className="wrapper style1 special">
            <div className="inner">
                <header className="major">
                    <h2>Tracking reports on internally displaced persons<br />
                    With full scale pipeline and processing.</h2>
                    <p>Features include: article retrieval, report extraction, <br />
                filtering, classNameification, information extraction, and visualization.</p>
                </header>
                <ul className="icons major">
                    <li><span className="icon fa-download major style2"><span className="label"></span></span></li>
                    <li><span className="icon fa-cogs major style2"><span className="label"></span></span></li>
                    <li><span className="icon fa-area-chart major style2"><span className="label"></span></span></li>
                    </ul>
                    </div>
        </section>
        <section id="two" className="wrapper alt style2">
            <section className="spotlight">
            <div className="image"><img src={pic1} alt="" /></div><div className="content">
            <h2>Article processing</h2>
        <p>We have built a customized web scraping infrastructure to retrieve articles and extract content into a SQL database.</p>
        </div>
        </section>
<section className="spotlight">
    <div className="image"><img src={pic2} alt="" /></div><div className="content">
    <h2>Natural Language</h2>
<p>A combination of natural language processing and keyword analysis is used to retrieve useful information from articles.</p>
</div>
</section>
<section className="spotlight">
    <div className="image"><img src={pic3} alt="" /></div><div className="content">
    <h2>Visual analysis</h2>
<p>A visual front-end interacts with the database to produce a map of displacement events, and highlight extracted information.</p>
</div>
</section>
<section className="spotlight">
    <div className="image"><img src={pic4} alt="" /></div><div className="content">
    <h2>Ready to go</h2>
<p>The tool is open source, built on Python, PostgreSQL, and Node.js, and fully Dockerized, for reliable deployment anywhere.</p>
</div>
</section>
</section>

<section id="three" className="wrapper style3 special">
    <div className="inner">
    <header className="major">
    <h2>Access Everything</h2>
<p>Challenge results, codebase and visualizations are all available to view.<br /></p>
</header>
<ul className="features">
    <li className="icon fa-github">
    <h3>GitHub Repository</h3>
<p>The <a href="https://github.com/Data4Democracy/internal-displacement">repository</a> that contains the open source code and notebooks for our solution.</p>
</li>
<li className="icon fa-check-square-o">
    <h3>Results</h3>
    <p>A <a href="https://www.dropbox.com/sh/500mvfi1y8rw9g9/AABUF216v6H8VnKloZlp-DvCa?dl=0">DropBox</a> folder containing the test set classNameification and information extraction results.</p>
</li>
<li className="icon fa-globe">
    <h3>Visualization Map</h3>
<p>Our <a href="http://d4d_idviz.yane.fr/">map visualization</a> prototype can be viewed here.</p>
</li>
<li className="icon fa-book">
    <h3>Documentation</h3>
    <p>See <a href="https://github.com/data4democracy/internal-displacement/wiki">here</a> for how to deploy and use the code for our article processing pipeline.</p>
</li>
</ul>
</div>
</section>
<section id="cta" className="wrapper style4">
    <div className="inner">
    <header>
    <h2>Want to join the team?</h2>
</header>
<ul className="actions vertical">
	<li><a href="datafordemocracy.slack.com" className="button fit">Sign Up!</a></li>
		</ul>
		</div>
		</section>

	</div>
);

// const HomePage = () => (
// 	<div id="page-wrapper">
// 		<div id="banner">
// 			<div className="inner">
// 				<h2>Internal Displacement</h2>
// 				<p>A Data for Democracy solution for the Unite Ideas IDETECT Challenge.</p>
// 			</div>
// 			Learn More
// 		</div>
//
// 		<div id="one" className="">
// 			<div className="inner">
// 				<div className="major">
// 					<h2>Tracking reports on internally displaced persons<br />
// 						With full scale pipeline and processing.</h2>
// 					<p>Features include: article retrieval, report extraction, <br />
// 						filtering, classification, information extraction, and visualization.</p>
// 				</div>
// 				<ul className="icons major">
// 					<li><span className="icon fa-download major style2"><span className="label"></span></span></li>
// 					<li><span className="icon fa-cogs major style2"><span className="label"></span></span></li>
// 					<li><span className="icon fa-area-chart major style2"><span className="label"></span></span></li>
// 				</ul>
// 			</div>
// 		</div>
//
//
// 		<div id="two" className="wrapper alt style2">
// 			<div className="spotlight">
// 				<div className="image"><img src={pic1} alt="" /></div><div className="content">
// 				<h2>Article processing</h2>
// 				<p>We have built a customized web scraping infrastructure to retrieve articles and extract content into a SQL database.</p>
// 			</div>
// 			</div>
// 			<div className="spotlight">
// 				<div className="image"><img src={pic2} alt="" /></div><div className="content">
// 				<h2>Natural Language</h2>
// 				<p>A combination of natural language processing and keyword analysis is used to retrieve useful information from articles.</p>
// 			</div>
// 			</div>
// 			<div className="spotlight">
// 				<div className="image"><img src={pic3} alt="" /></div><div className="content">
// 				<h2>Visual analysis</h2>
// 				<p>A visual front-end interacts with the database to produce a map of displacement events, and highlight extracted information.</p>
// 			</div>
// 			</div>
// 			<div className="spotlight">
// 				<div className="image"><img src={pic4} alt="" /></div><div className="content">
// 				<h2>Ready to go</h2>
// 				<p>The tool is open source, built on Python, PostgreSQL, and Node.js, and fully Dockerized, for reliable deployment anywhere.</p>
// 			</div>
// 			</div>
// 		</div>
//
// 		<div id="three" className="wrapper style3 special">
// 			<div className="inner">
// 				<header className="major">
// 					<h2>Access Everything</h2>
// 					<p>Challenge results, codebase and visualizations are all available to view.<br /></p>
// 				</header>
// 				<ul className="features">
// 					<li className="icon fa-github">
// 						<h3>GitHub Repository</h3>
// 						<p>The <a href="https://github.com/Data4Democracy/internal-displacement">repository</a> that contains the open source code and notebooks for our solution.</p>
// 					</li>
// 					<li className="icon fa-check-square-o">
// 						<h3>Results</h3>
// 						<p>A <a href="https://www.dropbox.com/sh/500mvfi1y8rw9g9/AABUF216v6H8VnKloZlp-DvCa?dl=0">DropBox</a> folder containing the test set classification and information extraction results.</p>
// 					</li>
// 					<li className="icon fa-globe">
// 						<h3>Visualization Map</h3>
// 						<p>Our <a href="http://d4d_idviz.yane.fr/">map visualization</a> prototype can be viewed here.</p>
// 					</li>
// 					<li className="icon fa-book">
// 						<h3>Documentation</h3>
// 						<p>See <a href="https://github.com/data4democracy/internal-displacement/wiki">here</a> for how to deploy and use the code for our article processing pipeline.</p>
// 					</li>
// 				</ul>
// 			</div>
// 		</div>
//
// 		<div id="cta" className="wrapper style4">
// 			<div className="inner">
// 				<header>
// 					<h2>Want to join the team?</h2>
// 				</header>
// 				<ul className="actions vertical">
// 					<li><a href="datafordemocracy.slack.com" className="button fit">Sign Up!</a></li>
// 				</ul>
// 			</div>
// 		</div>
//
// 		<footer id="footer">
// 			<ul className="icons">
// 				<li>
// 					<a target="_blank" href="https://twitter.com/data4democracy" className="icon fa-twitter">
// 					<span className="label">twitter</span>
// 					</a>
// 				</li>
//
//
// 				<li><a target="_blank" href="https://github.com/data4democracy/internal-displacement" className="icon fa-github"
// 				><span className="label">github</span></a></li>
//
// 			</ul>
// 			<ul className="copyright">
// 				<li>2017 Data for Democracy</li>
// 				<li>Design: <a href="http://html5up.net" target="_blank">HTML5 UP</a></li>
// 			</ul>
// 		</footer>
//
// 	</div>
//
// );

export default HomePage;