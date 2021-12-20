'use strict';

const e = React.createElement;

class AdvancedButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { advanced: false };
  }

  render() {
    if (this.state.advanced) {
      return e('button',
          { onClick: () => this.setState({advanced: false})},
          'Simple'
      );
    }

    return e(
      'button',
      { onClick: () => this.setState({ advanced: true }) },
      'Advanced'
    );
  }
}

const domContainer = document.querySelector('#advanced_search');
ReactDOM.render(e(AdvancedButton), domContainer);