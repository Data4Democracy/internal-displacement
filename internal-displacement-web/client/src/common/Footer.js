import React, {Component} from 'react';
import {render} from 'react-dom';

const Footer = () => (
    <footer id="footer">
        <ul className="icons">
            <li>
                <a target="_blank" href="https://twitter.com/data4democracy" className="icon fa-twitter">
                    <span className="label">twitter</span>
                </a>
            </li>


            <li>
                <a target="_blank" href="https://github.com/data4democracy/internal-displacement" className="icon fa-github">
                    <span className="label">github</span>
                </a>
            </li>

        </ul>
        <ul className="copyright">
            <li>2017 Data for Democracy</li>
            <li>Design: <a href="http://html5up.net" target="_blank">HTML5 UP</a></li>
        </ul>
    </footer>
);

export default Footer;