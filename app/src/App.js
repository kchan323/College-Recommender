import {Route, BrowserRouter as Router, Link, Switch} from "react-router-dom";
import Result from "./Results"
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

function App() {
  return (
    <Router>
    <div className="App">
      <header className="App-header">

      <Form>
        <Form.Group>
          <Form.Label>SAT Score</Form.Label>
          <Form.Control type="sat" placeholder="SAT Score" />
        </Form.Group>
        <Form.Group>
          <Form.Label>Size</Form.Label>
          {/* placeholder="Select school size" */}
          <Form.Control as="select">
            <option>Small</option>
            <option>Medium</option>
            <option>Large</option>
          </Form.Control>
        </Form.Group>
      </Form>


        <Link to="/result"> Results </Link>
        <Switch>
          <Route path="/result" component={Result}></Route>
        </Switch>
      </header>
    </div>
    </Router>
  );
}

export default App;
