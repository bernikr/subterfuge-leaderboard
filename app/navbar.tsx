import { Link, useLocation } from "@remix-run/react";
import { Button, Container, Form, Nav, Navbar } from "react-bootstrap";

export default function MyNavbar() {
  const location = useLocation();

  const menu_items = [
    {
      name: "Home",
      href: "/",
      current: location.pathname == "/",
    },
    {
      name: "About",
      href: "/about",
      current: location.pathname == "/about",
    },
  ];

  return (
    <Navbar
      expand="lg"
      className="navbar navbar-expand-md navbar-dark bg-dark mb-4"
    >
      <Container>
        <Navbar.Brand as={Link} to="/">
          Subterfuge Leaderboards
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            {menu_items.map((item) => (
              <Nav.Link
                as={Link}
                key={item.name}
                to={item.href}
                aria-current={item.current ? "page" : undefined}
                className={item.current ? "active" : ""}
              >
                {item.name}
              </Nav.Link>
            ))}
          </Nav>
          <Form className="d-flex" autoComplete="off" id="serachform">
            <div className="autocomplete me-2">
              <input
                id="search"
                className="form-control"
                type="search"
                placeholder="Search Players"
                aria-label="Search Players"
              />
            </div>
            <Button variant="outline-success" type="submit">
              Search
            </Button>
          </Form>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
