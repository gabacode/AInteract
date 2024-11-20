import Feed from "./components/organisms/Feed";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "./styles/index.scss";

export const App = () => {
  return (
    <>
      <div className="app">
        <Feed />
      </div>
      <footer className="footer">
        <div className="container">
          Powered by <a href="https://koucee.com">Koucee</a>
        </div>
      </footer>
    </>
  );
};
