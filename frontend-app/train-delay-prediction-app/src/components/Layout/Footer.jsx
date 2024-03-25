import React from "react";
import classes from './Footer.module.css';

const Footer = (props) => {
  return (
      <>
    <div style={{
        backgroundImage: `url(${require('../../assets/train-footer-1.jpg')})`,
        backgroundRepeat: 'repeat-x',
        width: '400%',
        height: 400,
        marginTop: 50
      }}>
    </div>
    </>
  );
};

export default Footer;