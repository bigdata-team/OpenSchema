import { useNavigate } from "react-router";
import { Button } from "@/components/ui/button";

function NotFound() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center px-6">
      <div className="text-center space-y-6">
        <div className="space-y-2">
          <h1 className="text-4xl font-extrabold tracking-tight">Oops!</h1>
          <p className="text-muted-foreground">The page you’re looking for doesn’t exist or has moved.</p>
        </div>

        <div className="flex items-center justify-center gap-3">
          <Button variant="secondary" onClick={() => navigate(-1)}>
            Go back
          </Button>
        </div>
      </div>
    </div>
  );
}

export default NotFound;
