
const e = React.createElement;

//
// this is hacky(using jquery inside react) and against the spirit of React, ... but it works...
// Probably I should rewrite the whole search page in react and get rid of the python templates
// or else use jquery exclusively.....
//

class AdvancedButton extends React.Component {
  constructor(props) {
    super(props);
    if ($('#search_mode').val() === 'simple') {
      this.state = { advanced: false };
    } else {
      this.state = { advanced: true };
    }
  }

  render() {
    this.toggleAdvancedSearchVisible()
    if (this.state.advanced) {
      return e('button',
          { onClick: () => { this.setState({advanced: false}); this.toggleAdvancedSearchVisible();}
          },
          'Simple'
      );
    }

    return e(
      'button',
      { onClick: () => { this.setState({ advanced: true });
                                  this.toggleAdvancedSearchVisible();} },
      'Advanced'
    );
  }

  toggleAdvancedSearchVisible() {
    if (this.state.advanced) {
      $('#search_mode').val("advanced");
      $('#advanced_search').show();
    } else {
      $('input:radio[name="format"][value="Any"]').prop('checked', true)
      $('input:radio[name="download_type"][value="Any"]').prop('checked', true);
      $('#search_mode').val("simple");
      $('#advanced_search').hide();
    }
  }
}

const buttonDomContainer = document.querySelector('#advanced_search_button');
ReactDOM.render(e(AdvancedButton), buttonDomContainer);

