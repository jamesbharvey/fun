
const e = React.createElement;

class AdvancedButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { advanced: false };
    this.toggleAdvancedSearchVisible()
  }

  render() {
    if (this.state.advanced) {
      return e('button',
          { onClick: () => { this.setState({advanced: false}); this.toggleAdvancedSearchVisible();}
          },
          'Advanced'
      );
    }

    return e(
      'button',
      { onClick: () => { this.setState({ advanced: true });
                                  this.toggleAdvancedSearchVisible();} },
      'Simple'
    );
  }
  //
  // this is hacky(using jquery inside react) and against the spirit of React, but I'm not redoing it right
  // Probably I should rewrite the whole search page in react and get rid of the python templates
  //

  toggleAdvancedSearchVisible() {
    if (this.state.advanced) {
      $('#advanced_search').show()
    } else {
      $('#advanced_search').hide()
    }
  }
}

const buttonDomContainer = document.querySelector('#advanced_search_button');
ReactDOM.render(e(AdvancedButton), buttonDomContainer);

