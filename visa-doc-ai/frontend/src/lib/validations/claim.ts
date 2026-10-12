export function validateClaim(claim: string): boolean {
  return Boolean(claim && claim.trim().length > 3);
}
