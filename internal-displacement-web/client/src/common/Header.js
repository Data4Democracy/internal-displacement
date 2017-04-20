import React from 'react';
import { Link, IndexLink } from 'react-router';
import {Navbar, Nav, NavItem} from 'react-bootstrap';

const navbarInstance = () => (
	<Navbar>
		<Navbar.Header>
			<Navbar.Brand>
				<IndexLink to="/" activeClassName="active">Home</IndexLink>
			</Navbar.Brand>
		</Navbar.Header>
		<Nav>
			<NavItem eventKey={1} href="#">Link</NavItem>
			<NavItem eventKey={2} href="#">Link</NavItem>
		</Nav>
	</Navbar>
);

export default navbarInstance;
