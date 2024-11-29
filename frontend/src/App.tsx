import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Feed } from "./components/organisms/Feed";
import { UserPage } from "./components/organisms/UserPage";

export const App = () => {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<Feed />} />
          <Route path="/:username" element={<UserPage />} />
          {/* <Route path="/post/:postId" element={<PostPage />} /> */}
        </Routes>
      </div>
      <footer className="footer"></footer>
    </Router>
  );
};
