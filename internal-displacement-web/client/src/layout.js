import Header from './common/Header';
import Footer from './common/Footer';
import React, {Component} from 'react';

class Layout extends Component {
    render() {
        return (
            <div>
                {this.props.children}
                <Footer />
            </div>
        )
    }
};

export default Layout;