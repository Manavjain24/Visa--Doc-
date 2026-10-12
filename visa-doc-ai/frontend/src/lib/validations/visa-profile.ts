export function validateVisaProfile(data: any): boolean {
  return Boolean(data.nationality && data.destination_country && data.visa_category);
}
