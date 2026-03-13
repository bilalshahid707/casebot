import axios from "axios";

export const authConfig = {
  pages: {
    signIn: "/auth/signin",
  },
  callbacks: {
    authorized({ auth, request: { nextUrl } }) {
      const isLoggedIn = !!auth?.user?.id;
      const isOnDashboard = nextUrl.pathname.startsWith("/dashboard");
      const isOnCases = nextUrl.pathname.startsWith("/cases");
      const isOnSignIn = nextUrl.pathname === "/auth/signin";

      if (isOnDashboard || (isOnCases && !isLoggedIn)) {
        Response.redirect(new URL("/auth/signin", nextUrl));
        return false;
      }
      if (isOnSignIn && isLoggedIn) {
        return Response.redirect(new URL("/dashboard", nextUrl));
      }
      return true;
    },

    async session({ session, token }) {
      if (!token?.accessToken) return null;

      // Since the session has its own expiry so we are validating user with the token on backend to make the session null
      try {
        const { data } = await axios.get(
          `${process.env.NEXT_PUBLIC_API_URL}/users/me`,
          {
            headers: { Authorization: `Bearer ${token.accessToken}` },
          },
        );
      } catch {
        return null;
      }

      session.user = session.user || {};
      session.user.id = token.id;
      session.user.username = token.username;
      session.accessToken = token.accessToken;

      return session;
    },
  },
  providers: [],
};
