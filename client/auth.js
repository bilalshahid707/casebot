import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import axios from "axios";
import { CredentialsSignin } from "@auth/core/errors";

class InvalidCredentialsError extends CredentialsSignin {
  code = "invalid_credentials";
}

class ServerError extends CredentialsSignin {
  code = "server_error";
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
      },
      authorize: async (credentials) => {
        const formData = new FormData();
        formData.append("username", credentials.username);
        formData.append("password", credentials.password);

        try {
          const { data } = await axios.post(
            `${process.env.NEXT_PUBLIC_API_URL}/auth/signin`,
            formData,
          );
          console.log(data);
          if (!data?.user) throw new InvalidCredentialsError();
          return {
            id: String(data?.user.id),
            username: data?.user.username,
            accessToken: data?.access_token,
            accessTokenExpires: data?.access_token_expires,
          };
        } catch (error) {
          if (error instanceof CredentialsSignin) throw error;

          const status = error?.response?.status;
          if (Number(status) === 401 || status === 403) {
            throw new InvalidCredentialsError();
          }
          throw new ServerError();
        }
      },
    }),
  ],

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        return {
          ...token,
          id: user.id,
          username: user.username,
          accessToken: user.accessToken,
          accessTokenExpires: token.exp,
        };
      }

      try {
        await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/users/me`, {
          headers: { Authorization: `Bearer ${token.accessToken}` },
        });
      } catch {
        return null;
      }
      if (Math.floor(Date.now() / 1000) > token?.exp) {
        return null;
      }

      return token;
    },

    async session({ session, token }) {
      // If jwt returned null, token will be empty — session will be invalid
      if (!token?.accessToken) return session;

      session.user = session.user || {};
      session.user.id = token.id;
      session.user.username = token.username;
      session.accessToken = token.accessToken;
      return session;
    },
  },

  pages: {
    signIn: "/auth/signin",
  },

  session: { strategy: "jwt" },
});
